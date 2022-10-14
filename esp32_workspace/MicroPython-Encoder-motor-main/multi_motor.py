from encoder_N20_esp import PID, Motor
import time

# Creating objects of each motor
m1 = Motor(32, 33, 25, 16, 4) # Motor(M1, M2, EN, C1, C2, frequency)
m2 = Motor(27, 14, 26, 17, 5) # Motor(M1, M2, EN, C1, C2, frequency) 
# Creating PID objects for each motor
p1 = PID(m1, 2.2, 0.21, 5, 800) #Kp,Kd,Ki
p2 = PID(m2, 2.2, 0.21, 5, 800)
while(1):
    
    #p1.setTarget(374/2+25) #374 ticks per rotation and 1:2 ratio transmition
    p2.setTarget(374)
    #p2.setSpeed(100)
        