from machine import Pin, ADC, PWM
from time import sleep
import streams

s=streams.serial()
led = Pin(26,Pin.OUT)
while True:
    led.value(1)
    sleep(1)
    led.value(0)
    sleep(1)
    line=s.readline()
    print(line)