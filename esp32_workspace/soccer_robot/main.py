from encoder_esp import PID, Motor
import time
import esp_server_hello_world
try:
  import usocket as socket
except:
  import socket
import ujson as json

# Creating objects of each motor
m1 = Motor(33, 32, 25, 4, 16) # Motor(M1, M2, EN, C1, C2, #frequency)
m2 = Motor(27, 14, 26, 17, 5) # Motor(M1, M2, EN, C1, C2, #frequency)

# Creating PID objects for speed control of each motor
p1 = PID(m1, 2.5, 0, 10, 250) #Kp,Kd,Ki,250RPM max speed of the motor.
p2 = PID(m2, 2.5, 0, 10, 250)


while(1):
    p1.setSpeed_L(5)
    p2.setSpeed_R(5)
    
    print("L/R: ", round(p1.vFilt_L,2), round(p2.vFilt_R,2))
    
    
    #m2.speed(0)
