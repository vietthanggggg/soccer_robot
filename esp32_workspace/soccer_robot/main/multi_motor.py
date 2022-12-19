from encoder_esp import PID, Motor
import time

m1 = Motor(33, 32, 25, 4, 16) # Motor(M1, M2, EN, C1, C2, #frequency)
m2 = Motor(14, 27, 26, 17, 5) # Motor(M1, M2, EN, C1, C2, #frequency)

# Creating PID objects for speed control of each motor
p1 = PID(m1, 2.5, 0, 10, 250) #Kp,Kd,Ki,250RPM max speed of the motor.
p2 = PID(m2, 2.5, 0, 10, 250)
m1.speed(0)
m2.speed(0)  

#p1.setTarget(10)
#p2.setTarget(10)

try:
    while(1):
        #Openloop table
        #1000 ~ 100 pwm ... 100~10 pwm
        #m1.speed(100) #10%pwm
        #p1.calrpm()#rpm
        
        #Respond closed loop PID
        #p1.setSpeed(50) #50rpm
        #p2.setSpeed(50) #50rpm
        

#thuc nghiem
        #p1.setTarget(100) #100 encoder counts
        #p2.setTarget(100) #100 encoder counts
    
except KeyboardInterrupt:
    # Press Ctrl+C to exit the application
    pass

# Exiting application (clean up)
m1.speed(0)
m2.speed(0)   
    