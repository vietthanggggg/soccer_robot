import socket

HOST = "192.168.0.12"  # The server's hostname or IP address
PORT = 80  # The port used by the server

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall("Hello world".encode())
#data = s.recv(1024)
#print(data.decode())
