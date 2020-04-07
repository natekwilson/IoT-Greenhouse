import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.IN)
GPIO.setup(2,GPIO.IN)

while True:
	print("External: " + str(GPIO.input(25)) + " Internal: " + str(GPIO.input(2)))
