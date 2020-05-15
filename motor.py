#!/usr/bin/python
import RPi.GPIO as GPIO
import time
 
#GPIO SETUP

MotorSpeed = 200

STBY = 4
AIN1 = 17
AIN2 = 27
PWMA = 22
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(STBY, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)

GPIO.output(STBY, GPIO.HIGH)
GPIO.output(AIN1, GPIO.HIGH)
GPIO.output(AIN2, GPIO.LOW)
GPIO.output(PWMA, GPIO.HIGH)
 
input = input("press key")
GPIO.output(STBY, GPIO.LOW)
GPIO.output(AIN1, GPIO.LOW)
GPIO.output(AIN2, GPIO.LOW)
GPIO.output(PWMA, GPIO.LOW)
