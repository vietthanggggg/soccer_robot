import socket
import json
import os

file = os.path.abspath("cv_workspace/field_processing/data.json")

HOST = "172.20.10.2"  # The server's hostname or IP address
PORT = 80  # The port used by the server

f=open(file)
data = json.load(f)

print(data["move_point_list"])

points = data["move_point_list"]
points = str(points)
points = points.encode()

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while(1):
    s.sendall(points)
    
print('Loop ended.')

#.sendall("G".encode())
#data = s.recv(1024)
#print(data.decode())
