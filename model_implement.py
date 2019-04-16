################################## KNN MODEL IMPLEMENTED ##############################
import urllib
import re
import requests
import RPi.GPIO as GPIO  #Importing all the required libraries
import serial
import time
import sys
import Adafruit_DHT
import numpy as np
import picamera
import time
import pandas as pd
import cv2
from sklearn import preprocessing, cross_validation, neighbors
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import accuracy_score
#import matplotlib.pyplot as plt
column=['time','temp','humidity','relay','rain','green_per','wind','moisture']
df=pd.read_csv(r'/var/www/html/dht.csv',header=None,names=column)
df.drop(['time'],1,inplace=True)
df2=df.mask(df.astype(object).eq('None')).dropna()
X=np.array(df2.drop(['relay'],axis=1))
y=np.array(df2['relay'])
X_train,X_test,y_train,y_test=cross_validation.train_test_split(X,y,test_size=0.1)
print('test'+str(y_test.shape))
print('train'+str(y_train.shape))
clf=neighbors.KNeighborsClassifier()
clf.fit(X_train,y_train)
accuracy=clf.score(X_test,y_test)
predict1=clf.predict(X_train)
#print(f1_score(y_train,, average='binary'))  
#average_precision_score(y_train,predict)  
#precision_score(y_train, predict, average='macro')
with picamera.PiCamera() as cam:
	cam.resolution=(1024,768)
	cam.start_preview()
	time.sleep(5)
	cam.capture('/home/pi/Desktop/still.jpg')
	cam.capture('/var/www/html/still.jpg')
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
	GPIO.setmode(GPIO.BOARD)
	ser=serial.Serial('/dev/ttyACM0')                 # to connect arduinopi
#	file=open("dht11.csv","w")
	GPIO.setwarnings(False)
	GPIO.setup(13,GPIO.IN)
	GPIO.setup(5,GPIO.IN)
	GPIO.setup(11,GPIO.OUT)
	RAIN=GPIO.input(5)                                #Variable to store the Raining Status
	relay=GPIO.input(13)                              #Variable to store the on/off of relay
	#t=time.asctime(time.localtime(time.time()))       #Variable stores the current time
	humidity,temperature = Adafruit_DHT.read_retry(11,2)
	a=ser.readline()
	wind=requests.get("https://api.thingspeak.com/apps/thinghttp/send_request?api_key=RVRML8PD68G61SIB")
	file=open("/var/www/html/dht.csv","a")                          #Opening File in the Append Mode
	#GPIO.output(11,True)
	#file.write(str(t))
	#file.write(",")
	#print(str(t))
	#file.write(str(temperature))
	#file.write(",")
	print('temp'+str(temperature))
	#file.write(str(humidity))
	#file.write(",")
	print('humidity'+str(humidity))
	#file.write(str(relay))
	#file.write(",")
	#print('relay'+str(relay))
	#file.write(str(RAIN))
	#file.write(",")
	print('rain'+str(RAIN))
	#file.write(str(per))
	#file.write(",")
	print('pergreen'+str(per))
	#file.write(str(wind.text))
	#file.write(",")
	print('wind'+str(wind.text))
	#file.write(str(a))
	print('moisture'+str(a))
	#file.write("\n")
	#file.close()
	#time.sleep(4)
	#GPIO.output(11,False)
	#print("data written")
	#for k in range(0,5):
	#	print("waiting for"+' '+str(k)+' '+'second')
	#	time.sleep(1)
	test = np.array([temperature, humidity, RAIN, per, str(wind.text), a])
	arr = test.reshape(1, -1)
	predict=clf.predict(arr)
	print("Status of the relay should be:")
	print(predict)
        print(accuracy_score(y_train, predict1))

GPIO.cleanup()

