import threading
import time
import os
import RPi.GPIO as GPIO
import Adafruit_DHT
import json
import requests

def takeSnapShot():
    dataDict = {}
    print ("This loops on a timer every %d minutes" % snapshotInterval)
    t = time.strftime("%Y%m%d-%H%M%S")
    title = time.strftime("%m-%d-%H:%M")
    print(title)
    imgPathString = ''

    #Take Image if it's the beginning of a 30minute interval
    if imageCounter == 1:
        imgPathString = (t + ".jpg")
        captureCMD = "raspistill -q 10 -o /home/pi/greenhouse-logs/images/%s" % (imgPathString)
        sendCMD = "scp /home/pi/greenhouse-logs/images/%s ec2-user@iotgreenhouse.natewilsonit.com:greenhouse-logs/%s" %  (imgPathString,imgPathString)
        os.system(captureCMD)
        os.system(sendCMD)

    #BCM GPIO PIN ROLE ASSIGNMENTS 
    internalLight = 25
    externalLight = 2
    moisture = 18
    humidTemp = 3

    #INITIALIZE AND SETUP EACH PIN
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(internalLight,GPIO.IN)
    GPIO.setup(externalLight,GPIO.IN)
    GPIO.setup(moisture, GPIO.IN)
    DHT_SENSOR = Adafruit_DHT.DHT11

    #READ IN VALUES
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, humidTemp)

    #ASSINGN VALUES TO dataDict DICTIONARY OBJECT
    dataDict['temp'] = temperature
    dataDict['humid'] = humidity
    dataDict['moisture'] = GPIO.input(moisture)
    dataDict['intLight'] = GPIO.input(internalLight)
    dataDict['extLight'] =GPIO.input(externalLight)
    dataDict['imgPath'] = imgPathString
    dataDict['title'] = title
    
    #PRINT DATADict
    print("External: " + str(GPIO.input(externalLight))+" Internal: "+ str(GPIO.input(internalLight)))
    print("Temp: " + str(temperature) + " Humidity: " + str(humidity))
    print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    print("Moisture: " + str(GPIO.input(moisture)))

    #WRITE JSON DATADict OBJECT
    with open('snapshot.json', 'w') as outfile:
        json.dump(dataDict, outfile)
    
    print(dataDict)
    print("Beginning POST request")
    url = 'http://iotgreenhouse.natewilsonit.com:9000/api/items'
    result = requests.post(url, json = json.dump(dataDict))
    print(result)

def startTimer():
    global imageCounter
    global imageInterval
    global snapshotInterval
    if imageCounter < imageInterval:
        imageCounter += 1
    elif imageCounter == imageInterval:
        imageCounter = 0
    threading.Timer((snapshotInterval * 60 ), startTimer).start()
    takeSnapShot()
    
#Every SNAPSHOTINTERVAL minutes make a snapshot JSON object
#Every IMAGEINTERVAL snapshots, capture and image
#append that JSON object to a text file and send to the AWS server
#send image file via SCP

snapshotInterval = 1
imageInterval = 2
imageCounter = 0

startTimer()