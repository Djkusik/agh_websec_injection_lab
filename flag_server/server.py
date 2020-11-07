import sys
import socket
import signal
import argparse
import threading

from chat_enums import ServerMessage, ClientMessage


class ThreadedServer:
    banned_nick = ['zakazany', 'SERVER']

    def __init__(self, host=socket.gethostname(), port=5555):
        self.host = host
        self.port = port
        self.clients = {}

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
                    conn.send(ServerMessage.connection_established.name.encode('utf-8'))
                    print(f"{nick} connected to the server from {ip}:{port}")
                    return nick
        except:
            print(f"Something went wrong when registering new client from {ip}:{port}")
            return None

    def client_tcp(self, conn, addr):
        nick = self.register_client(conn, addr)
        if nick is not None:
            self.broadcast("SERVER", f"{nick}>Hello chat! I joined here")
            try:
                while True:
                    msg = conn.recv(4096).decode('utf-8')
                    print(f"TCP MSG - {nick}::{msg}")
                    
                    if msg.startswith(ClientMessage.exit.name):
                        del self.clients[nick]
                        break
                    self.broadcast(nick, msg)
            except:
                del self.clients[nick]
            print(f"{nick} left the chat :(")
            self.broadcast("SERVER", f"{nick}>Goodbye chat, I went offline")
        conn.close()

    def client_udp(self):
        while True:
            bytes_msg, address = self.socket_udp.recvfrom(8192)
            msg = str(bytes_msg, 'utf-8')
            msg = msg.split("::")
            nick = msg[0]
            msg = "::".join(msg[1::])
            print(f"UDP MSG - {nick}::{msg}")
            self.broadcast(nick, msg)

    def broadcast(self, src_nick, msg):
        f_msg = f"{src_nick}::{msg}"
        for t_client in self.clients:
            if t_client != src_nick:
                self.clients[t_client][0].sendall(f_msg.encode('utf-8'))

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
    args = p.parse_args()
    host = args.host
    port = args.port

    return host, port

def main():
    host, port = parse_args()
    ThreadedServer(host, port).listen()

if __name__ == '__main__':
    main()