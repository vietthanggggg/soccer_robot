from machine import Pin,Timer
import network,usys
from time import sleep_ms
import urequests as requests
import ujson as json
try:
  import usocket as socket
except:
  import socket

def do_connect():
    with open("/wifi_settings.json") as credentials_json:
        settings = json.loads(credentials_json.read())
    headers = {"Content-Type":"application/json"}
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
  

