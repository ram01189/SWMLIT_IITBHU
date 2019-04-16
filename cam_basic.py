######################### Basic Code of Camera Capture ########################
import numpy as np
import cv2
cap=cv2.VideoCapture(0)
ret,frame=cap.read()
img2=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
print(img2)
cv2.imshow('image',img2)
cv2.waitkey(0)
cap.release()
import numpy as np
import cv2
cap=cv2.VideoCapture(0)
ret,frame=cap.read()
img2=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
print(img2)
cv2.imshow('image',img2)
cv2.waitkey(0)
cap.release()
cv2.destroyAllWindows()
cv2.destroyAllWindows()

