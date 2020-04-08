import threading
import time
import os
import RPi.GPIO as GPIO
import Adafruit_DHT

#Main time loop

#Every 2 minutes make a snapshot JSON object
#Every 15 snapshots, capture and image
#append that JSON object to a text file and send to the AWS server
#send image file via SCP

snapshotInterval = 2
imageInterval = 15
imageCounter = 0

def takeSnapShot():
    data = {}
    print ("This loops on a timer every %d minutes" % interval)
    t = time.strftime(format["%b%d%Y%H:%M",time.localtime(time.time())])
    #Take Image if it's the beginning of a 30minute interval
    imgPathString = ''
    if imageCounter == 0:
        os.system("raspistill -q 10 -o /home/pi/greenhouse-logs/images/%s.jpg" (t))
        imgPathString = (t + ".jpg")
        os.system("scp -i /home/pi/AWS-AL2.pem /home/pi/greenhouse-logs/images/%s ec2-user@iotgreenhouse.natewilsonit.com:greenhouse-logs/%s" (imgPathString,imgPathString))
    

    internalLight = 25
    externalLight = 2
    moisture = 18
    humidTemp = 27

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(internalLight,GPIO.IN)
    GPIO.setup(externalLight,GPIO.IN)
    GPIO.setup(moisture, GPIO.IN)
    DHT_SENSOR = Adafruit_DHT.DHT11

    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    data['temp'] = temperature
    data['humid'] = humidity
    data['moisture'] = GPIO.input(moisture)
    data['intLight'] = GPIO.input(internalLight)
    data['extLight'] =GPIO.input(externalLight)
    data['imgPath'] = imgPathString
    
    print("External: " + str(GPIO.input(externalLight))+" Internal: "+ str(GPIO.input(internalLight)))
    print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    print(GPIO.input(moisture))
    #Make 
    with open('snapshot.json', 'w') as outfile:
		json.dump(data, outfile)    



def startTimer():
    threading.Timer((snapshotInterval * 60 ), startTimer).start()
    takeSnapShot()
    if (imageCounter < imageInterval )
        imageCounter = imageCounter + 1
    elif (imageCounter == imageInterval)
        imageCounter = 0
