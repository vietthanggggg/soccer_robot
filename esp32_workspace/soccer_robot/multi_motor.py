from encoder_esp import PID, Motor
import time

# Creating objects of each motor
m1 = Motor(33, 32, 25, 4, 16) # Motor(M1, M2, EN, C1, C2, #frequency)
m2 = Motor(14, 27, 26, 17, 5) # Motor(M1, M2, EN, C1, C2, #frequency)

# Creating PID objects for speed control of each motor
p1 = PID(m1, 2.5, 0, 10, 250) #Kp,Kd,Ki,250RPM max speed of the motor.
p2 = PID(m2, 2.5, 0, 10, 250)
try:
    while(1):
        #p1.setSpeed_L(30)
        #p2.setSpeed_R(30)
        print("L/R: ", round(p1.vFilt_L,2), round(p2.vFilt_R,2))
        m2.speed(50)
        m1.speed(50)
    
except KeyboardInterrupt:
    # Press Ctrl+C to exit the application
    pass

# Exiting application (clean up)
m1.speed(0)
m2.speed(0)   
    