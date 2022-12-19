from time import sleep_ms, ticks_us
from machine import Pin, PWM, disable_irq, enable_irq


# A class for functions related to motors
class Motor:
    
    # Instance variable for keeping the record of the encoder position
    pos = 0
    

    # Interrupt handler
    def handle_interrupt(self,pin):
        a = self.px.value()
        if a > 0:
            self.pos = self.pos+1
        else:
            self.pos = self.pos-1
            
    
        
    
    # Constroctor for initializing the motor pins
    def __init__(self,m1, m2, en, c1, c2, freq=50):
        self.px = Pin(c1, Pin.IN)
        self.py = Pin(c2, Pin.IN)
        self.freq = freq
        self.p_in1 = Pin(m1, Pin.OUT)
        self.p_in2 = Pin(m2, Pin.OUT)
        self.p_en = PWM(Pin(en,Pin.OUT), freq)
        # Interrupt initialization
        self.py.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt)
    
    # Arduino's map() function implementation in python 
    def convert(self, x, i_m, i_M, o_m, o_M):
        return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)

    # A function for speed control without feedback(Open loop speed control)
    def speed(self,M):
        pwm = self.convert(abs(M),0, 1000, 0, 1000)
        #print(pwm)
        self.p_en.duty(pwm)
        if M>0:
            self.p_in1(1)
            self.p_in2(0)
        else:
            self.p_in1(0)
            self.p_in2(1)

# A class for closed loop speed and postion control
class PID:
    
    # Instance variable for this class
    posPrev = 0

    # Constructor for initializing PID values
    def __init__(self, M, kp=2.5, kd=0, ki=10, umaxIn=500, eprev=0, eintegral=0):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.M = M                   # Motor object
        self.umaxIn  =umaxIn
        self.eprev = eprev
        self.eintegral = eintegral
        self.vFilt=0
        self.vPrev=0
        

    # Function for calculating the Feedback signal. It takes the current value, user target value and the time delta.
    def evalu(self,value, target, deltaT):
        
        # Propotional
        e = target-value 

        # Derivative
        dedt = (e-self.eprev)/(deltaT)

        # Integral
        self.eintegral = self.eintegral + e*deltaT
        
        # Control signal
        u = self.kp*e + self.kd*dedt + self.ki*self.eintegral
        
        # Direction and power of  the control signal
        if u > 0:
            if u > self.umaxIn:
                u = self.umaxIn
            else:
                u = u
        else:
            if u < -self.umaxIn:
                u = -self.umaxIn
            else:
                u = u 
        self.eprev = e
        
        
        return u
    
    # Function for closed loop position control
    def setTarget(self,target):
        
        # Time delta is predefined as we have set a constat time for the loop.(Initial dealy is 
        # very high,interfers with response time)(Integral part becomes very high due to huge deltaT value at the beginning)
        # Use tick_us() to calculate the delay manually(remove slee_ms() if you use realtime delay)
        deltaT = .01

        # Disable the interrupt to read the position of the encoder(encoder tick)               
        state = disable_irq()
        step = self.M.pos

        # Enable the intrrupt after reading the position value
        enable_irq(state)

        # Control signal call
        x = int(self.evalu(step, target, deltaT))
        
        # Set the speed 
        self.M.speed(x)
        print(step, target) # For debugging
        
        # Constant delay 
        sleep_ms(10)
        
    # Function for closed loop speed control
    def setSpeed(self, target):
        state = disable_irq()
        posi = self.M.pos
        enable_irq(state)

        # Delta is high because small delta causes drastic speed stepping.
        deltaT = .1

        # Target RPM
        vt = target 

        # Current encoder tick rate
        velocity = (posi - self.posPrev)/deltaT
        self.posPrev = posi

        # Converted to RPM
        # 350 ticks per revolution of output shaft of the motor 
        # For different gearing differnt values
        # Run the function without setting the motor speed and calculate the ticks per revolution by manually rotaing the motor  
        #v = velocity*60/374
        v = velocity*60/(400/2)
        
        self.vFilt = 0.854*self.vFilt + 0.0728*v + 0.0728*self.vPrev
        self.vPrev = v
        
        # Call for control signal
        x = int(self.evalu(self.vFilt, vt, deltaT))

        # Set the motor speed
        self.M.speed(x)
        print(self.vFilt, vt)   # For debugging
        v=self.vFilt
        # Constant delay
        sleep_ms(100)
        

        
        
    def calrpm(self):
        state = disable_irq()
        posi = self.M.pos
        enable_irq(state)

        # Delta is high because small delta causes drastic speed stepping.
        deltaT = .1
 

        # Current encoder tick rate
        velocity = (posi - self.posPrev)/deltaT
        self.posPrev = posi

        # Converted to RPM
        # 350 ticks per revolution of output shaft of the motor 
        # For different gearing differnt values
        # Run the function without setting the motor speed and calculate the ticks per revolution by manually rotaing the motor  
        #v = velocity*60/374
        v = velocity*60/(374/2)
        print(v)
        
        # Set the motor speed
        #self.M.speed(M)
        sleep_ms(100)