#!/usr/local/bin/python
#import RPi.GPIO as GPIO
from gpiozero import LightSensor
import urllib.request
import json
import sys
import subprocess
import os

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(4, GPIO.OUT)


lightSensor1 = LightSensor(4)
lightSensor2 = LightSensor (20)
lightSensor3 = LightSensor (27)
lightSensor4 = LightSensor (13)
lightSensor5 = LightSensor (18)


#GPIO.setup(4, GPIO.IN)

#GPIO.add_event_detect(4,GPIO.FALLING, timeout = 50000)
#GPIO.add_event_callback(4, GPIO.FALLING, callback=inputChng, bouncetime=3)    

        
movie1 = ("/home/pi/Downloads/30seconds/snow301.mp4")
movie2 = ("/home/pi/Downloads/30seconds/cloud30.mp4")
movie3 = ("/home/pi/Downloads/30seconds/rain301.mp4")
movie4 = ("/home/pi/Downloads/30seconds/sun301.mp4")
movie5 = ("/home/pi/Downloads/30seconds/black30.mp4")


##def inputChng():
##    global omxp
##    global globalvar
##    print('globa')
##    print(globalvar)
##    if (globalvar==1):
##        print ('quit')
##        omxp.kill()
##        globalvar =0
##    print ('exits')


global sensortouched 


globalvar = 0
sensortouched = None

    
responseWeather = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast?id=2673722&APPID=bfb8163bad72d71e9da0c72974a73828').read()
jsonResponse = json.loads(responseWeather.decode('utf-8'))
weatherNow  = jsonResponse['list'][0]
weatherinNextThreeHours  = jsonResponse['list'][1]
weatherinNextSixHours  = jsonResponse['list'][2]
weatherinNextNineHours  = jsonResponse['list'][3]
weatherinNextTwelveHours  = jsonResponse['list'][4]
                

def playVideo (currentForecast):
    global globalvar 
    globalvar = 1
    global omxp
    
    if currentForecast == 'Clear':
        print ("The weather is clear!")
        #omxp = subprocess.Popen(['omxplayer','--win','100 100 200 200',movie4],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=False)
        omxp = subprocess.Popen(['omxplayer','--win','200 200 500 500',movie4])
        print (omxp.pid)
    if currentForecast == 'Rain':
        print ("The weather is rain!")
        #omxp = subprocess.Popen(['omxplayer','--win','100 100 200 200',movie3],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=False)
        omxp = subprocess.Popen(['omxplayer','--win','200 200 500 500',movie3])
        print (omxp.pid)
    if currentForecast == 'Clouds':
        print ("The weather is clouds!")
        #omxp = subprocess.Popen(['omxplayer','--win','100 100 200 200',movie2],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=False)
        omxp = subprocess.Popen(['omxplayer','--win','200 200 500 500',movie2])
        print (omxp.pid)
    if currentForecast == 'Snow':
        print ("The weather is snow!")
        #omxp = subprocess.Popen(['omxplayer','--win','100 100 200 200',movie1],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=False)
        omxp = subprocess.Popen(['omxplayer','--win','200 200 500 500',movie1])
    if currentForecast == 'Nothing':
        print ("Black screen to be displayed")
        #omxp = subprocess.Popen(['omxplayer','--win','100 100 200 200',movie5],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=False)
        omxp = subprocess.Popen(['omxplayer','--win','200 200 500 500',movie5])
    return 


#Sensor 1 and 2 are light (Use Case: Both are touched at Begining) 
if (lightSensor1.light_detected and lightSensor2.light_detected and lightSensor3.light_detected and lightSensor4.light_detected and lightSensor5.light_detected and sensortouched==None):
    if (globalvar==1):
        print ('quit when any sensor is touched', omxp.pid)
        os.system('killall omxplayer.bin')
        globalvar =0
    sensortouched = None
    playVideo ("Nothing")
        
##lightSensor1.when_dark=inputChng()
##lightSensor1.when_light=inputChng()
##lightSensor2.when_dark=inputChng()
##lightSensor2.when_light=inputChng()


while True:
    print(lightSensor1.value)
    print(lightSensor2.value)
    print(lightSensor3.value)
    print(lightSensor4.value)
    print(lightSensor5.value)
        
    if lightSensor1.wait_for_dark(1) and sensortouched != 1:
        if (globalvar==1):
            print ('quiting when sensor1 touched, I am killing' , omxp.pid)
            #omxp.stdin.write(´q´)
            os.system('killall omxplayer.bin')
            globalvar =0     
        print ("Sensor 1 is touched")
        sensortouched = 1
        CurrentresponseWeather = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?id=2673730&APPID=bfb8163bad72d71e9da0c72974a73828').read()
        print( CurrentresponseWeather)
        CurrentjsonResponse = json.loads(CurrentresponseWeather.decode('utf-8'))
        currentForecast = CurrentjsonResponse['weather'][0]['main']
        print(currentForecast)
        playVideo (currentForecast)
  

    if lightSensor2.wait_for_dark(1) and sensortouched != 2:
        if (globalvar==1):
            print ('quiting when sensor2 touched, I am killing' , omxp.pid)
            os.system('killall omxplayer.bin')
            globalvar =0
        print ("Sensor 2 is touched")
        sensortouched = 2
        currentForecast = weatherinNextThreeHours['weather'][0]['main']
        playVideo (currentForecast)

    if lightSensor3.wait_for_dark(1) and sensortouched != 3:
        if (globalvar==1):
            print ('quiting when sensor3 touched, I am killing' , omxp.pid)
            os.system('killall omxplayer.bin')
            globalvar =0
        print ("Sensor 3 is touched")
        sensortouched = 3
        currentForecast = weatherinNextSixHours['weather'][0]['main']
        playVideo (currentForecast)

    if lightSensor4.wait_for_dark(1) and sensortouched != 4:
        if (globalvar==1):
            print ('quiting when sensor4 touched, I am killing' , omxp.pid)
            os.system('killall omxplayer.bin')
            globalvar =0
        print ("Sensor 4 is touched")
        sensortouched = 4
        currentForecast = weatherinNextNineHours['weather'][0]['main']
        playVideo (currentForecast)

    if lightSensor5.wait_for_dark(1) and sensortouched != 5:
        if (globalvar==1):
            print ('quiting when sensor5 touched, I am killing' , omxp.pid)
            os.system('killall omxplayer.bin')
            globalvar =0
        print ("Sensor 5 is touched")
        sensortouched = 5
        currentForecast = weatherinNextNineHours['weather'][0]['main']
        playVideo (currentForecast)
            
    
    #Sensor 1 and 2 are light (Use Case: Both are touched) 
    if (lightSensor1.light_detected and lightSensor2.light_detected and lightSensor3.light_detected and lightSensor4.light_detected and lightSensor5.light_detected and sensortouched!=None):
        if (globalvar==1):
            print ('quit when any sensor is touched', omxp.pid)
            os.system('killall omxplayer.bin')
            globalvar =0
        sensortouched = None
        playVideo ("Nothing")

        



    





        

          
