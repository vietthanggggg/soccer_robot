from time import sleep_ms, ticks_us
from machine import Pin, PWM, disable_irq, enable_irq

class Motor:
    pos=0
    def __init__(self,m1, m2, c1, c2):
        self.px = Pin(c1, Pin.IN)
        self.py = Pin(c2, Pin.IN)
        self.p_in1 = Pin(m1, Pin.OUT)
        self.p_in2 = Pin(m2, Pin.OUT)
        # Interrupt initialization
        self.py.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt)
    # Interrupt handler
    def handle_interrupt(self,pin):
        a = self.px.value()
        if a > 0:
            self.pos = self.pos+1
        else:
            self.pos = self.pos-1
        print(a)
        
# Creating objects of each motor
m1 = Motor(32, 33, 16, 4) # Motor(M1, M2, EN, C1, C2, #frequency)
encx=Pin(16, Pin.IN)
ency=Pin(4 , Pin.IN)
while True:
    print(encx.value(),ency.value())
    sleep_ms(10)
    
    #print(step) 