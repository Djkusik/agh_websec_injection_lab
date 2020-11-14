import sys
import socket
import signal
import argparse
import threading
import os
import json
import traceback
import dotenv

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from common.chat_enums import ServerMessage, ClientMessage
from common.ascii_art import arts
from common.models import *

dotenv.load_dotenv()
PASSWORD = os.environ.get("FLAG_DB_PASSWORD", 'admin1234')

class Server:
    banned_nick = ['SERVER', 'admin']

    def __init__(self, host=socket.gethostname(), port=5555, init_db=False, pathflags='./flags.json'):
        self.host = host
        self.port = port
        self.clients = {}
        self.udp_flag = os.environ.get('UDP_FLAG', 'bit{udp_temporary}')
        
        try:
            db_engine = self.init_engine()
            self.db_sess = self.init_session(db_engine)
            if init_db:
                print("Initializing DB for first time")
                self.init_db(db_engine)
                flags = self.read_flags(pathflags)
                self.add_flags(flags)
        except:
            print("Database said bye bye and something went wrong")
            traceback.print_exc()
            sys.exit(1)

        print(f"Initializing chat server on {host}:{port}")
        self.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            self.socket_tcp.bind((host, port))
            self.socket_udp.bind((host, port))
        except:
            print(f"Failed when binding on {host}:{port}")
            sys.exit(1)
        
        print("Succesfully initialized")

    def init_db(self, engine):
        Base.metadata.create_all(engine)

    def init_engine(self):
        return create_engine(f'postgresql://telepathy:{PASSWORD}@localhost/telepathy')

    def init_session(self, engine):
        Session = sessionmaker(autocommit=False, autoflush=True)
        Session.configure(bind=engine)
        return Session()

    def read_flags(self, pathfile):
        try:
            with open(pathfile) as f:
                flags = json.loads(f.read())
        except FileNotFoundError:
            print(f'File {pathfile} not found')
            sys.exit(1)
        return flags

    def add_flags(self, flags):
        for item in flags:
            task = Task(
                name=item['taskname'], 
                lab_no=item['lab_no'],
                flag=item['flag'],
                points=item['points']
            )
            try:
                task = self.db_sess.add(task)
                self.db_sess.commit()
            except IntegrityError as e:
                self.db_sess.rollback()
                sys.exit(1)

    def listen(self):
        print("Starting listening...")
        self.socket_tcp.listen(5)
        try:
            while True:
                conn, addr = self.socket_tcp.accept()
                self.t_tcp = threading.Thread(target=self.client_tcp, args=(conn, addr))
                self.t_udp = threading.Thread(target=self.client_udp)
                self.t_tcp.setDaemon(True)
                self.t_udp.setDaemon(True)
                self.t_tcp.start()
                self.t_udp.start()

        except KeyboardInterrupt:
            print("\nClosing server")
        except:
            print("\nSomething went wrong when listening")
        finally:
            self.close()

    def register_client(self, conn, addr):
        ip = addr[0]
        port = addr[1]
        try:
            while True:
                nick = conn.recv(64).decode('utf-8')
                if nick == '' or nick in self.banned_nick:
                    print(f"{nick} tried to connect from {ip}:{port}")
                    conn.send(ServerMessage.nick_invalid.name.encode('utf-8'))

                elif nick in self.clients:
                    print(f"User from {ip}:{port} tried to use taken nickname: {nick}")
                    conn.send(ServerMessage.nick_taken.name.encode('utf-8'))

                else:
                    self.clients[nick] = [conn, ip, port]
                    conn.send(ServerMessage.nick_correct.name.encode('utf-8'))
                    print(f"{nick} connected to the server from {ip}:{port}")
                    return nick
        except:
            print(f"Something went wrong when registering new client from {ip}:{port}")
            return None

    def client_tcp(self, conn, addr):
        nick = self.register_client(conn, addr)
        if nick is not None:
            self.clients[nick][0].sendall(arts[0].encode('utf-8'))
            self.broadcast("SERVER", f"{nick}>Hello everyone! I joined here")
            try:
                while True:
                    msg = conn.recv(4096).decode('utf-8')
                    print(f"TCP MSG - {nick}::{msg}")
                    
                    if msg.startswith(ClientMessage.exit.name):
                        del self.clients[nick]
                        break
                    elif msg.startswith('Stats'):
                        self.show_stats(nick, msg)
                    elif msg.startswith('R'):
                        self.try_register(nick, msg)
                    elif msg.startswith('S'):
                        self.try_solve(nick, msg)
                    elif msg.startswith('L'):
                        self.list_tasks(nick, msg)
                    elif msg.startswith('M'):
                        self.broadcast(nick, msg)
                    else:
                        pass
            except:
                self.clients[nick][0].send(ServerMessage.exit.name.encode('utf-8'))
                traceback.print_exc()
                del self.clients[nick]
            print(f"{nick} left the chat :(")
            self.broadcast("SERVER", f"{nick}>Goodbye chat, I went offline")
        conn.close()

    def client_udp(self):
        while True:
            msg, address = self.socket_udp.recvfrom(1024)
            print(f"UDP MSG - {address}::{str(msg, 'utf-8')}")
            answer = str.encode(self.udp_flag)
            self.socket_udp.sendto(answer, address)

    def broadcast(self, src_nick, msg):
        f_msg = f"{src_nick}::{msg}"
        for t_client in self.clients:
            if t_client != src_nick:
                self.clients[t_client][0].sendall(f_msg.encode('utf-8'))

    def try_register(self, nick, msg):
        try:
            password = msg.split(' ')[1]
        except (ValueError, IndexError):
            self.clients[nick][0].send(ServerMessage.password_empty.name.encode('utf-8'))
            return
        if self.register(nick, password):
            self.clients[nick][0].send(ServerMessage.registered.name.encode('utf-8'))
        else:
            self.clients[nick][0].send(ServerMessage.user_already_registered.name.encode('utf-8'))

    def register(self, nick, password):
        user = User(name=nick, password=password)
        try:
            user = self.db_sess.add(user)
            self.db_sess.commit()
            return True
        except IntegrityError as e:
            self.db_sess.rollback()
            return False

    def try_solve(self, nick, msg):
        try:
            code, password, taskname, flag = msg.split(' ')
        except ValueError:
            self.clients[nick][0].send(ServerMessage.message_incorrect.name.encode('utf-8'))
            return
        reply = self.solve(nick, password, taskname, flag)
        self.clients[nick][0].send(reply)
        
    def solve(self, nick, password, taskname, flag):
        user = self.db_sess.query(User).filter(and_(User.name == nick, User.password == password)).first()
        if user is None:
            return ServerMessage.password_incorrect.name.encode('utf-8')

        task = self.db_sess.query(Task).filter(Task.name == taskname).first()
        if task is None:
            return ServerMessage.wrong_task.name.encode('utf-8')
        if task.flag != flag:
            return ServerMessage.invalid_flag.name.encode('utf-8')

        if any([task.name == taskname for task in user.tasks]):
            return ServerMessage.solved_already.name.encode('utf-8')

        user.tasks.append(task)
        self.db_sess.commit()
        return ServerMessage.task_solved.name.encode('utf-8')

    def list_tasks(self, nick, msg):
        try:
            lab_no = int(msg.split(' ')[1])
        except (ValueError, IndexError):
            self.clients[nick][0].send(ServerMessage.wrong_lab_no.name.encode('utf-8'))
        if lab_no not in range(1, 5):
            self.clients[nick][0].send(ServerMessage.wrong_lab_no.name.encode('utf-8'))
        reply = ''
        for task in self.db_sess.query(Task).filter(Task.lab_no == lab_no).all():
            reply += f'{task}\n'
        
        self.clients[nick][0].sendall(reply.encode('utf-8'))

    def show_stats(self, nick, msg):
        try:
            mode = int(msg.split(' ')[1])
        except ValueError:
            self.clients[nick][0].send(ServerMessage.wrong_stats_mode.name.encode('utf-8'))
        if mode not in range(1, 3):
            self.clients[nick][0].send(ServerMessage.wrong_stats_mode.name.encode('utf-8'))
        reply = ''
        if mode == 1:
            for user in self.db_sess.query(User).all():
                reply += f'{user}\n'
        elif mode == 2:
            try:
                taskname = msg.split(' ')[2]
            except (ValueError, IndexError):
                self.clients[nick][0].send(ServerMessage.wrong_task.name.encode('utf-8'))
            solutions = self.db_sess.query(Solution).filter(Solution.task.has(Task.name == taskname)).order_by(Solution.solve_time.asc()).all()
            if len(solutions) > 0:
                reply += f'Solutions for {solutions[0].task}\n'
                for i, solution in enumerate(solutions):
                    reply += f'{i+1}. {solution.user.name} -> {solution.solve_time}\n'
            else:
                reply += 'Lack of solutions for this task now'
        self.clients[nick][0].sendall(reply.encode('utf-8'))

    def add_task(self, taskname, lab_no, flag, points):
        task = Task(name=taskname, lab_no=lab_no, flag=flag, points=points)
        try:
            task = self.db_sess(task)
            self.db_sess.commit()
        except IntegrityError as e:
            self.db_sess.rollback()
            raise

    def close(self):
        self.disc_clients()
        self.socket_tcp.close()
        self.socket_udp.close()
        print("Disconnected every client and closed both sockets")
        sys.exit(0)

    def disc_clients(self):
        if self.clients:
            for client in self.clients:
                try:
                    self.clients[client][0].sendall(ServerMessage.exit.name.encode('utf-8'))
                except:
                    print(f"Problem when closing connection to the {client}")
                    pass
        else:
            pass


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('-ht', '--host', help='Host address to bind', type=str, default=socket.gethostname())
    p.add_argument('-p', '--port', help='Server port to bind', type=int, default=5555)
    p.add_argument('-idb', '--init-db', help='True to init db for first time', action='store_true')
    p.add_argument('-f', '--flags', help='Path to JSON file with flags', type=str, default='./flags.json')
    args = p.parse_args()
    host = args.host
    port = args.port
    init_db = args.init_db
    flags = args.flags

    return host, port, init_db, flags

def main():
    host, port, init_db, flags= parse_args()
    Server(host, port, init_db, flags).listen()

if __name__ == '__main__':
    main()