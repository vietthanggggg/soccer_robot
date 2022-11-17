from encoder_esp import PID, Motor
import time
import esp_server_hello_world
try:
  import usocket as socket
except:
  import socket

# Creating objects of each motor
m1 = Motor(33, 32, 25, 4, 16) # Motor(M1, M2, EN, C1, C2, #frequency)
m2 = Motor(27, 14, 26, 17, 5) # Motor(M1, M2, EN, C1, C2, #frequency) 
# Creating PID objects for each motor

p1 = PID(m1, 2.5, 0, 10, 100) #Kp,Kd,Ki for speed control
p2 = PID(m2, 2.7, 0, 10, 100)
#do_connect()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("172.20.10.2", 90))
s.listen(5)
conn, addr = s.accept()
print('Got a connection from %s' % str(addr))

while(1):  
    request = conn.recv(1024)
    print(request.decode())
    if(request.decode()=="G"):
        p1.setSpeed_L(50)
        p2.setSpeed_R(50)
    elif(request.decode()=="D"):
        p1.setSpeed_L(-50)
        p2.setSpeed_R(-50)
    elif(request.decode()=="R"):
        p1.setSpeed_L(50)
        p2.setSpeed_R(-50)
    elif(request.decode()=="L"):
        p1.setSpeed_L(-50)
        p2.setSpeed_R(50)
    elif(request.decode()=="0"):
        m1.speed(0)
        m2.speed(0)
    elif(request.decode()=="C"):
        m1.speed(0)
        m2.speed(0)
        conn.close()
        break
    
   