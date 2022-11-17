from encoder_N20_esp import PID, Motor
import time

# Creating objects of each motor
m1 = Motor(32, 33, 25, 16, 4) # Motor(M1, M2, EN, C1, C2, #frequency)
while True:
    m1.speed(200)
    #print(m1.pos)
    time.sleep(0.5)