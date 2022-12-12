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

start_time = time.time_ns()
while True:
    t = time.time_ns()
    dt = t - start_time
    start_time = t
    
    request = conn.recv(1024)
    x = request.decode()
    request = conn.recv(1024)
    y = request.decode()
    request = conn.recv(1024)
    theta = request.decode()
    request = conn.recv(1024)
    array_of_goals = request.decode()
    
    print("x:"+ x+", y:"+ y+", theta:"+theta)
    print(array_of_goals)
    dt=dt/1000000000
    print("dt= "+ str(dt))
