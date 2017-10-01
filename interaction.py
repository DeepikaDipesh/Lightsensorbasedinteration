#!/usr/local/bin/python
from gpiozero import LightSensor
import urllib.request
import json
import sys
from subprocess import Popen
from time import sleep

lightSensor1 = LightSensor(26)
lightSensor2 = LightSensor (4)
        
movie1 = ("/home/pi/Videos/movie1.mp4")
movie2 = ("/home/pi/Downloads/finalcloud.mp4")
movie3 = ("/home/pi/Downloads/rainy.mp4")
movie4 = ("/home/pi/Downloads/sunny.mp4")


while True:
        if lightSensor1.wait_for_dark(2):
                print ("It is dark")
                responseWeather = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast?id=2673722&APPID=bfb8163bad72d71e9da0c72974a73828').read()
                jsonResponse = json.loads(responseWeather.decode('utf-8'))
                #print(jsonResponse)
                temperature = float(jsonResponse['main']['temp'])
                weatherNow  = jsonResponse['list'][0]
                weatherinNextThreeHours  = jsonResponse['list'][1]
                weatherinNextSixHours  = jsonResponse['list'][2]
                weatherinNextNineHours  = jsonResponse['list'][3]
                todayforecast = weatherNow['weather'][0]['main']
                if todayforecast == 'Clear':
                        print ("The weather is clear!")
                        #omxp = Popen(['omxplayer',movie4])
                if todayforecast == 'Rain':
                        print ("The weather is rain!")
                        #omxp = Popen(['omxplayer',movie3])
                if todayforecast == 'Clouds':
                        print ("The weather is clouds!")
                        #omxp = Popen(['omxplayer',movie2])
                if todayforecast == 'Snow':
                        print ("The weather is snow!")
                        #omxp = Popen(['omxplayer',movie1]) 

        if lightSensor1.wait_for_light(2):
                print ("It is light")
                print(lightSensor1.value)
                print ("lightSensor1_Successs")

        #Sensor 1 and 2 are dark (Use Case: Both are touched) 
        if not (lightSensor1.light_detected and lightSensor2.light_detected):
                print("Both the sensors are dark")





        

          
