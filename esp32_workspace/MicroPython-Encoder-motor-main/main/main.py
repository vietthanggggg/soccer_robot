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

# Creating PID objects for speed control of each motor
p1 = PID(m1, 2.5, 0, 10, 250) #Kp,Kd,Ki,250RPM max speed of the motor.
p2 = PID(m2, 2.5, 0, 10, 250)

# Initialize localization in cm
wheel_radius = 4.3
wheel_base = 10

x=0
y=0
theta=0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("172.20.10.2", 90))
s.listen(5)
conn, addr = s.accept()
print('Got a connection from %s' % str(addr))

while(1):
    request = conn.recv(1024)
    print(request.decode())
    #p1.setSpeed_L(50)
    #p2.setSpeed_R(50)
    #print("L/R: ", round(p1.vFilt_L,2), round(p2.vFilt_R,2))
    #m2.speed(0)