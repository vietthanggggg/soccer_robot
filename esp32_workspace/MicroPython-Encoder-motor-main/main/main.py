from encoder_esp import PID, Motor
import time
import localization

# Creating objects of each motor
m1 = Motor(33, 32, 25, 4, 16) # Motor(M1, M2, EN, C1, C2, #frequency)
m2 = Motor(27, 14, 26, 17, 5) # Motor(M1, M2, EN, C1, C2, #frequency)

# Creating PID objects for speed control of each motor
p1 = PID(m1, 2.5, 0, 10, 250) #Kp,Kd,Ki,250RPM max speed of the motor.
p2 = PID(m2, 2.5, 0, 10, 250)



# Initialize localization in cm
wheel_radius = 4.3
wheel_base = 10

last_left_dir = 1
last_right_dir = 1

odo = localization.odometry()
#stControl = stateControl.stateControl()
x=0
y=0
theta=0


try:
    start_time = time.time_ns()
    while True:
        t = time.time_ns()
        dt = t - start_time
        start_time = t
        
        odo.step()
        x, y , theta = odo.getPose()
        print(x)
        print(y)
        print(theta)
        
        break
    
except KeyboardInterrupt:
    # Press Ctrl+C to exit the application
    pass