import math
import espSocket
try:
  import usocket as socket
except:
  import socket
import ujson as json
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("172.20.10.2", 70))
s.listen(5)
conn, addr = s.accept()
print('Got a connection from %s' % str(addr))

request = conn.recv(1024)
array_of_goals = request.decode()
print(array_of_goals)
conn.sendall('ok'.encode())


start_time = time.time_ns()
while True:
    t = time.time_ns()
    dt = t - start_time
    start_time = t
    
    request = conn.recv(6)
    x = request.decode()
    conn.sendall('ok'.encode())
    request = conn.recv(6)
    y = request.decode()
    conn.sendall('ok'.encode())
    request = conn.recv(5)
    theta = request.decode()
    conn.sendall('ok'.encode())
    
    
    print("x:"+ x+", y:"+ y+", theta:"+theta)
    dt=dt/1000000000
    print("dt= "+ str(dt))
