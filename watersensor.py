#!/usr/bin/python
import RPi.GPIO as GPIO
import time
 
#GPIO SETUP
channel = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
 

 
# infinite loop
while True:
        
        time.sleep(1)
