import socket
import sys


def get_udp_flag(host, port):
    msgToServer = "Hello there Server!"
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    socket_tcp.connect((host, port))
    socket_udp.sendto(bytes(msgToServer, 'utf-8'), (host, port))
    reply_flag, address = socket_udp.recvfrom(1024)
    print(str(reply_flag, 'utf-8'))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'{sys.argv[0]} [host] [port]')
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    get_udp_flag(host, port)
