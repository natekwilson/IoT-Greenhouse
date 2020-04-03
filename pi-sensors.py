import threading
import time
import os
import RPi.GPIO as GPIO


#Main time loop

#Every 2 minutes make a snapshot JSON object
#Every 15 snapshots, capture and image
#append that JSON object to a text file and send to the AWS server
#send image file via SCP


snapshotInterval = 2
imageInterval = 15
imageCounter = 0



def takeSnapShot():
    print "This loops on a timer every %d minutes" % interval
    t = time.strftime(format["%b%d%Y%H:%M",time.localtime(time.time())])
    #Take Image if it's the beginning of a 30minute interval
    if (imageCounter == 0)
        os.system("raspistill -q 25 -o /home/pi/greenhouse-logs/images/%s.jpg" (t))
    
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
