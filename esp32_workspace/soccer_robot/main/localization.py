import math
import espSocket
try:
  import usocket as socket
except:
  import socket
import ujson as json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("172.20.10.2", 70))
s.listen(5)
conn, addr = s.accept()
print('Got a connection from %s' % str(addr))

class odometry():

    def __init__(self):
        '''
            Initialize odometry
            
        '''
        self.x = 0
        self.y = 0
        self.theta = 0
        self.array_of_goals=0
        
    def getGoals(self):
        '''
            Call this function periodically to update robot pose estimiation.
        '''
        # LISTENNING FROM SOCKET
        request = conn.recv(1024)
        self.array_of_goals = request.decode()
        
        #Convert str to float and list
        self.array_of_goals = eval(self.array_of_goals)
        conn.sendall('ok'.encode())
            
        
        return self.array_of_goals
                
    def step(self):
        '''
            Call this function periodically to update robot pose estimiation.
        '''
        # LISTENNING FROM SOCKET
        request = conn.recv(6)
        self.x = request.decode()
        conn.sendall('ok'.encode())
        request = conn.recv(6)
        self.y = request.decode()
        conn.sendall('ok'.encode())
        request = conn.recv(5)
        self.theta = request.decode()
        conn.sendall('ok'.encode())
        #request = conn.recv(1024)
        #self.array_of_goals = request.decode()
        
        #Convert str to float and list
        self.x = float(self.x)
        self.y = float(self.y)
        self.theta = float(self.theta)
        #self.array_of_goals = eval(self.array_of_goals)
            
        
        return self.x, self.y, self.theta #, self.array_of_goals
        
    def resetPose(self):
        self.x = 0
        self.y = 0
        self.theta = 0
    
    def getPose(self):
        return self.x, self.y, self.theta #self.array_of_goals