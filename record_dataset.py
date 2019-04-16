##############################################Code to Record Dataset#############################
import os
import subprocess
import time
import urllib
import re
import requests
import RPi.GPIO as GPIO  #Importing all the required libraries
import serial
import time
import sys
import Adafruit_DHT
import numpy as np
import cv2
while(1):
	os.system('./webcam.sh')
	a=cv2.imread('still.jpg')           #reading an image from file
	print("image captured")
	#a=cv2.resize(im,None,fx=0.15,fy=0.15,interpolation=cv2.INTER_AREA)  #Reducing the size of an image
	hsv=cv2.cvtColor(a,cv2.COLOR_BGR2HSV) #converting image to hsv
	image_mask=cv2.inRange(hsv,np.array([20,50,50]),np.array([100,255,255])) # applying masking to detect the green colour 
	out=cv2.bitwise_and(a,a,mask=image_mask) # performing and operation with image and mask to show green area of image
	kernel = np.ones((5,5),np.uint8)
	dilation = cv2.dilate(image_mask,kernel,iterations = 2) #dilating the making image
	dil=dilation.ravel() # to convert the multidimensional array to the 1d array
	count = 0
	for x in np.nditer(dil):
		if (x==255):
                	count=count+1  # number of white pixels
	total=float(np.size(dil)) # total number of pixels 
	c=float(count) 
	p=c/total 
	per=p*100  #calculating the percentage of the green pixels
	print(per)
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	ser=serial.Serial('/dev/ttyACM0')
	GPIO.setup(13,GPIO.IN) 
	GPIO.setup(5,GPIO.IN)
	GPIO.setup(11,GPIO.OUT)
	RAIN=GPIO.input(5)                                #Variable to store the Raining Status
	relay=GPIO.input(13)                              #Variable to store the on/off of relay
	t=time.asctime(time.localtime(time.time()))       #Variable stores the current time
	humidity,temperature = Adafruit_DHT.read_retry(11,2)
	a=ser.readline()
	wind=requests.get("https://api.thingspeak.com/apps/thinghttp/send_request?api_key=RVRML8PD68G61SIB")
	file=open("/var/www/html/dht.csv","a")                          #Opening File in the Append Mode
	GPIO.output(11,True)
	file.write(str(t))
	file.write(",")
	print(str(t))
	file.write(str(temperature))
	file.write(",")
	print('temp'+str(temperature))
	file.write(str(humidity))
	file.write(",")
	print('humidity'+str(humidity))
	file.write(str(relay))
	file.write(",")
	print('relay'+str(relay))
	file.write(str(RAIN))
	file.write(",")
	print('rain'+str(RAIN))
	file.write(str(per))
	file.write(",")
	print('pergreen'+str(per))
	file.write(str(wind.text))
	file.write(",")
	print('wind'+str(wind.text))
	file.write(str(a))
	print('moisture'+str(a))
	#file.write("\n")
	file.close()
	time.sleep(4)
	GPIO.output(11,False)
	ser.write('end')
	print("end")
	for k in range(0,5):
		print("waiting for"+' '+str(k)+' '+'second')
		time.sleep(1)

GPIO.cleanup()

