import socket
import json
import os
import time

file = os.path.abspath("field_ComputerVision\data.json")

HOST = "172.20.10.2"  # The server's hostname or IP address
PORT = 90  # The port used by the server

f=open(file)
data = json.load(f)




robot_x = data["robot_x"]
robot_x = str(robot_x)
robot_x = robot_x.encode()

robot_y = data["robot_y"]
robot_y = str(robot_y)
robot_y = robot_y.encode()

robot_theta = data["robot_theta"]
robot_theta = str(robot_theta)
robot_theta = robot_theta.encode()

points = data["move_point_list"]
points = str(points)
points = points.encode()


s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.sendall(robot_x)
time.sleep(1)
s.sendall(robot_y)
time.sleep(1)
s.sendall(robot_theta)
time.sleep(1)

print('SENDED!') 

#s.sendall("G".encode())
#data = s.recv(1024)
#print(data.decode())
