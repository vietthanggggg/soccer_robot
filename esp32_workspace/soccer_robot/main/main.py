from encoder_esp import PID, Motor
import time
import localization
import stateControl

# Creating objects of each motor
m1 = Motor(33, 32, 25, 4, 16) # Motor(M1, M2, EN, C1, C2, #frequency)
m2 = Motor(14, 27, 26, 17, 5) # Motor(M1, M2, EN, C1, C2, #frequency)

# Creating PID objects for speed control of each motor
p1 = PID(m1, 2.5, 0, 10, 250) #Kp,Kd,Ki,250RPM max speed of the motor.
p2 = PID(m2, 2.5, 0, 10, 250)

m1.speed(0)
m2.speed(0)
# Initialize localization in cm
wheel_radius = 4.3
wheel_base = 10.5

last_left_dir = 1
last_right_dir = 1

odo = localization.odometry()
stControl = stateControl.stateControl()

x=0
y=0
theta=0
array_of_goals=0

array_of_goals = odo.getGoals()

try:
    start_time = time.time_ns()
    while True:
        t = time.time_ns()
        dt = t - start_time
        #print(dt)
        start_time = t

        odo.step()
        x, y , theta = odo.getPose()
        #print(x,y,theta)
        # Set inputs for the state machine
        
        stControl.input.x = x
        stControl.input.y = y
        stControl.input.theta = theta
        stControl.input.dt = dt
        stControl.input.array_of_goals= array_of_goals
        stControl.input.L = wheel_base
        stControl.input.radius = wheel_radius
        stControl.step()
        
        
        #print(stControl.output.left_motor)
        
        m1.speed(int(stControl.output.right_motor))
        m2.speed(int(stControl.output.left_motor)) 
       

except KeyboardInterrupt:
    # Press Ctrl+C to exit the application
    pass

# Exiting application (clean up)
m1.speed(0)
m2.speed(0)