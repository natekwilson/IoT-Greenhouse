#!/usr/bin/python
import RPi.GPIO as GPIO
import time
 
#GPIO SETUP

MotorSpeed = 200

STBY = 4
AIN1 = 17
AIN2 = 27
PWMA = 22
GPIO.setmode(GPIO.BOARD)
GPIO.setup(STBY, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PMWA, GPIO.OUT)

GPIO.output(STBY, GPIO.HIGH)
GPIO.output(AIN1, GPIO.HIGH)
GPIO.output(AIN2, GPIO.LOW)

GPIO.PWM(PMWA, MotorSpeed)
 
# infinite loop
while True:
        time.sleep(1)
