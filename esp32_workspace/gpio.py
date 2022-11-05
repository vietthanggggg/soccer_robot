import machine
led = machine.Pin(2,machine.Pin.OUT)
#led.on()


while True:
    command=input()
    print(command)
    if command=="1":
        led.on()
    else:
        led.off()