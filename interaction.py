#!/usr/local/bin/python
#import RPi.GPIO as GPIO
from gpiozero import LightSensor
import urllib.request
import json
import sys
import subprocess

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(4, GPIO.OUT)


lightSensor1 = LightSensor(4)
lightSensor2 = LightSensor (20)


#GPIO.setup(4, GPIO.IN)

#GPIO.add_event_detect(4,GPIO.FALLING, timeout = 50000)
#GPIO.add_event_callback(4, GPIO.FALLING, callback=inputChng, bouncetime=3)    

        
movie1 = ("/home/pi/Videos/movie1.mp4")
movie2 = ("/home/pi/Downloads/finalcloud.mp4")
movie3 = ("/home/pi/Downloads/rainy.mp4")
movie4 = ("/home/pi/Downloads/sunny.mp4")
movie5 = ("/home/pi/Downloads/black.mp4")


def inputChng():
    global omxp
    global globalvar
    print('globa')
    print(globalvar)
    if (globalvar==1):
        print ('quit')
        omxp.kill()
        globalvar =0
    print ('exits')

globalvar =0

    
responseWeather = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast?id=2673722&APPID=bfb8163bad72d71e9da0c72974a73828').read()
jsonResponse = json.loads(responseWeather.decode('utf-8'))
weatherNow  = jsonResponse['list'][0]
weatherinNextThreeHours  = jsonResponse['list'][1]
weatherinNextSixHours  = jsonResponse['list'][2]
weatherinNextNineHours  = jsonResponse['list'][3]
                

def playVideo (currentForecast):
    global globalvar
    globalvar = 1
    global omxp 
    if currentForecast == 'Clear':
        print ("The weather is clear!")
        omxp = subprocess.Popen(['omxplayer','--win','100 100 200 200',movie4],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
        print (omxp.pid)
    if currentForecast == 'Rain':
        print ("The weather is rain!")
        omxp = subprocess.Popen(['omxplayer','--win','100 100 200 200',movie3],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
        print (omxp.pid)
    if currentForecast == 'Clouds':
        print ("The weather is clouds!")
        omxp = subprocess.Popen(['omxplayer','--win','100 100 200 200',movie2],shell=False)
        print (omxp.pid)
    if currentForecast == 'Snow':
        print ("The weather is snow!")
        omxp = subprocess.Popen(['omxplayer','--win','100 100 200 200',movie1],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    if currentForecast == 'Nothing':
        print ("The weather is snow!")
        omxp = subprocess.Popen(['omxplayer','--win','100 100 200 200',movie5],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    return

lightSensor1.when_dark=inputChng()
lightSensor1.when_light=inputChng()
lightSensor2.when_dark=inputChng()
lightSensor2.when_light=inputChng()

while True:
    print(lightSensor1.value)
    print(lightSensor2.value)
        
    if lightSensor1.wait_for_dark(5):
        if (globalvar==1):
            print ('quiting when sensor1 touched, I am killing' + oxmp.pid)
            omxp.kill()
            globalvar =0
        print ("Sensor 1 is touched")
        currentForecast = weatherNow['weather'][0]['main']
        playVideo (currentForecast)
  

    if lightSensor2.wait_for_dark(5):
        if (globalvar==1):
            print ('quiting when sensor2 touched, I am killing' + oxmp.pid)
            omxp.kill()
            globalvar =0
        #omxp.stdin.write('q')
        print ("Sensor 2 is touched")
        currentForecast = weatherinNextThreeHours['weather'][0]['main']
        playVideo (currentForecast)
             
    
    #Sensor 1 and 2 are dark (Use Case: Both are touched) 
    if (lightSensor1.light_detected and lightSensor2.light_detected):
        if (globalvar==1):
            print ('quit when sensor2 is touched')
            omxp.kill()
            globalvar =0
        playVideo ("Nothing")
        print ("Black screen to be displayed")



    





        

          
