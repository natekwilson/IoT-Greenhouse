import threading
import time
import os
import RPi.GPIO as GPIO
import Adafruit_DHT
import json



#Every SNAPSHOTINTERVAL minutes make a snapshot JSON object
#Every IMAGEINTERVAL snapshots, capture and image
#append that JSON object to a text file and send to the AWS server
#send image file via SCP

snapshotInterval = 1
imageInterval = 2
imageCounter = 0


def takeSnapShot():
    data = {}
    print ("This loops on a timer every %d minutes" % snapshotInterval)
    t = time.strftime("%Y%m%d-%H%M%S")
    imgPathString = ''

    #Take Image if it's the beginning of a 30minute interval
    if imageCounter == 0:
        imgPathString = (t + ".jpg")
        captureCMD = "raspistill -q 10 -o /home/pi/greenhouse-logs/images/%s.jpg" % (imgPathString)
        sendCMD = "scp -i /home/pi/AWS-AL2.pem /home/pi/greenhouse-logs/images/%s ec2-user@iotgreenhouse.natewilsonit.com:greenhouse-logs/%s" %  (imgPathString,imgPathString)
        os.system(captureCMD)
        os.system(sendCMD)

    #BCM GPIO PIN ROLE ASSIGNMENTS 
    internalLight = 25
    externalLight = 2
    moisture = 18
    humidTemp = 27

    #INITIALIZE AND SETUP EACH PIN
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(internalLight,GPIO.IN)
    GPIO.setup(externalLight,GPIO.IN)
    GPIO.setup(moisture, GPIO.IN)
    DHT_SENSOR = Adafruit_DHT.DHT11

    #READ IN VALUES
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, humidTemp)

    #ASSINGN VALUES TO data DICTIONARY OBJECT
    data['temp'] = temperature
    data['humid'] = humidity
    data['moisture'] = GPIO.input(moisture)
    data['intLight'] = GPIO.input(internalLight)
    data['extLight'] =GPIO.input(externalLight)
    data['imgPath'] = imgPathString
    
    #PRINT DATA
    print("External: " + str(GPIO.input(externalLight))+" Internal: "+ str(GPIO.input(internalLight)))
    print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    print(GPIO.input(moisture))

    #WRITE JSON DATA OBJECT
    with open('snapshot.json', 'w') as outfile:
        json.dump(data, outfile)

def startTimer():
    threading.Timer((snapshotInterval * 60 ), startTimer).start()
    takeSnapShot()
    if imageCounter < imageInterval:
        imageCounter = imageCounter + 1
    elif imageCounter == imageInterval:
        imageCounter = 0

startTimer()