import socket

HOST = "172.20.10.2"  # The server's hostname or IP address
PORT = 90  # The port used by the server

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while(1):
    msg=input("Input: ")
    s.sendall(msg.encode())
    if msg == "C":
        s.close()
        break
print('Loop ended.')   

#.sendall("G".encode())
#data = s.recv(1024)
#print(data.decode())
