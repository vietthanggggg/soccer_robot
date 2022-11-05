from machine import Pin

led = Pin(2, Pin.OUT)

class Led:
    def __init__(self, state):
        self.state = state
    def states(self):
        if(self.state == "1"):
            led.value(1)
            print("LED ON")
        else:
            led.value(0)
            print("LED OFF")
            
while True:
    input_state = input()
    led_input = Led(input_state)
    led_input.states()
    
        
    
    