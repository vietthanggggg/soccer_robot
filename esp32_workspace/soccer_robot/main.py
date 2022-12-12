from encoder_esp import PID, Motor
import time


# Creating objects of each motor
m1 = Motor(33, 32, 25, 4, 16) # Motor(M1, M2, EN, C1, C2, #frequency)
m2 = Motor(27, 14, 26, 17, 5) # Motor(M1, M2, EN, C1, C2, #frequency)

# Creating PID objects for speed control of each motor
p1 = PID(m1, 2.5, 0, 10, 250) #Kp,Kd,Ki,250RPM max speed of the motor.
p2 = PID(m2, 2.5, 0, 10, 250)

try:
    while(1):
        m1.speed(30)
        m2.speed(30)
        #p1.setSpeed_R(50)
        #p2.setSpeed_L(50)
    
        #print("L/R: ", round(p2.vFilt_L,2), round(p1.vFilt_R,2))
    
except KeyboardInterrupt:
    # Press Ctrl+C to exit the application
    pass
    #m2.speed(0)
m1.speed(0)
m2.speed(0)
