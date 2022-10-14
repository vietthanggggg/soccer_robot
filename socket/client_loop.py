import socket
import time

HOST = "172.20.10.3"  # The server's hostname or IP address
PORT = 80  # The port used by the server

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    #Send LED on
    s.sendall("1".encode())
    data = s.recv(1024)
    time.sleep(1)
    print(data.decode())
    #Send LED off
    s.sendall("0".encode())
    data = s.recv(1024)
    time.sleep(1)
    print(data.decode())
    

#data = s.recv(1024)
#print(data.decode())
