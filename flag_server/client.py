import sys
import socket
import struct
import argparse
import threading

from common.chat_enums import ServerMessage, ClientMessage


class Client:
    quit_opt = ['exit', 'quit', 'q', 'kill', 'close']
    help_opt = ['help', 'h']

    def __init__(self, host=socket.gethostname(), port=5555):
        self.host = host
        self.port = port
        self.is_running = True
        
        print(f"Initializing chat client to the server on {host}:{port}")

        self.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket_tcp.connect((self.host, self.port))
        except:
            print(f"Failed when connecting to the {self.host}:{self.port}")
            sys.exit(1)

        print("Succesfully connected")
        self.nick = self.set_nick()

    def set_nick(self):
        try:
            while self.is_running:
                nick = input("Give your nickname: ")
                if nick == '':
                    continue
                self.socket_tcp.sendall(nick.encode('utf-8'))

                msg = self.socket_tcp.recv(1024).decode('utf-8')
                if msg == ServerMessage.nick_correct.name:
                    return nick

                elif msg == ServerMessage.nick_taken.name:
                    print(f"{nick} is already taken")

                elif msg == ServerMessage.nick_invalid.name:
                    print(f"{nick} is invalid")

                else:
                    print("Something went wrong. Try again")
        except KeyboardInterrupt:
            self.close()
        except SystemExit:
            sys.exit(0)
        except:
            pass

    def run(self):  
        try:
            self.t_tcp = threading.Thread(target=self.listen_tcp)
            self.t_talk = threading.Thread(target=self.talk_terminal)
            self.t_tcp.setDaemon(True)
            self.t_talk.setDaemon(True)
            self.t_tcp.start()
            self.t_talk.start()
            self.t_talk.join()

        except KeyboardInterrupt:
            self.close()
        except SystemExit:
            sys.exit(0)
        except:
            pass

    def listen_tcp(self):
        try:
            while self.is_running:
                msg = self.socket_tcp.recv(1024).decode('utf-8')
                if msg == '':
                    continue
                if msg == ServerMessage.exit.name:
                    print("\nServer sent disconnection signal")
                    self.is_running = False
                    sys.exit(0)
                self.print_msg(msg)
        except KeyboardInterrupt:
            self.close()
        except SystemExit:
            sys.exit(0)
        except:
            pass

    def talk_terminal(self):
        try:
            while self.is_running:
                usr_input = input(f"{self.nick}> ")
                if usr_input in self.quit_opt:
                    usr_input = ClientMessage.exit.name
                    self.close()
                elif usr_input in self.help_opt:
                    self.print_help()
                else:
                    self.socket_tcp.sendall(usr_input.encode('utf-8'))
        except KeyboardInterrupt:
            self.close()
        except SystemExit:
            sys.exit(0)
        except:
            pass

    def print_msg(self, msg):
        print("\r" + msg, f"\n{self.nick}> ", end='')

    def print_help(self):
        print("M [message]\t\t- to send message over TCP socket [broadcast]")
        print("R [password]\t\t- to register your nickname")
        print("S [password] [taskname] [flag] - try to solve task")
        print("L [lab_no]\t\t- list tasks")
        print("Stats 1\t\t - show users statistics")
        print("Stats 2 [taskname]\t- show task statistics")
        print(*self.quit_opt, "\t- to close chat", sep=" ")
        print(*self.help_opt, "\t\t\t- to print this help", sep=" ")

    def close(self):
        self.is_running = False
        self.disc_from_server()
        self.socket_tcp.close()
        self.socket_udp.close()
        print("Client is now closed")
        sys.exit(0)

    def disc_from_server(self):
        self.socket_tcp.sendall(ClientMessage.exit.name.encode('utf-8'))
        print("\nDisconnected from the server")        

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('-ht', '--host', help='Server address', type=str, default=socket.gethostname())
    p.add_argument('-p', '--port', help='Server port', type=int, default=5555)
    args = p.parse_args()
    host = args.host
    port = args.port

    return host, port

def main():
    host, port = parse_args()
    Client(host, port).run()

if __name__ == '__main__':
    main()