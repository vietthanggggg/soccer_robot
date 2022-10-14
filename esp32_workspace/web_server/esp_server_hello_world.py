from machine import Pin,Timer
import network,usys
import urequests as requests
import ujson as json
try:
  import usocket as socket
except:
  import socket
import _thread as threading

with open("/wifi_settings.json") as credentials_json:
    settings = json.loads(credentials_json.read())
headers = {"Content-Type":"application/json"}

def do_connect():
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(settings["wifi_name"], settings["password"])#connect to the station using
                                                                 #credentials from json file
        while not wlan.isconnected():
            pass
        print('network config:', wlan.ifconfig())
wlan = network.WLAN(network.STA_IF)     #ESP32 as an station,use STA_IF

do_connect()

if wlan.isconnected() == True:
    print("Connected")
    #print("My IP address: ",wlan.ifconfig()[0])
else:
    print("Not connected")
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.0.12", 80))
s.listen(5)
while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print(request.decode())
  conn.sendall('Hello world'.encode())
  #request = conn.recv(1024)
  #request = str(request)
  #print('Content = %s' % request)
  conn.close()
  break
  

