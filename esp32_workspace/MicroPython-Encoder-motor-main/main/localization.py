import math
import esp_server_hello_world
try:
  import usocket as socket
except:
  import socket
import ujson as json
import localization

class odometry():

    def __init__(self):
        '''
            Initialize odometry
            
        '''
        
        self.x = 0
        self.y = 0
        self.theta = 0
    
    def checking_connect():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("172.20.10.2", 90))
        s.listen(5)
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        

    def step(self):
        '''
            Call this function periodically to update robot pose estimiation.
        '''
        # LISTENNING FROM SOCKET
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("172.20.10.2", 90))
        s.listen(5)
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        
        request = conn.recv(1024)
        self.x = request.decode()
        request = conn.recv(1024)
        self.y = request.decode()
        request = conn.recv(1024)
        self.theta = request.decode() 
        
        return self.x, self.y, self.theta
        
    def resetPose(self):
        self.x = 0
        self.y = 0
        self.theta = 0
    
    def getPose(self):
        return self.x, self.y, self.theta