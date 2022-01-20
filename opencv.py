import cv2
import numpy as np
import math
import random



img=cv2.imread('./sprites/road.jpg')

#Grayscale image
#img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#Edge detector
img=cv2.Canny(img,350,350)


kernel=np.ones((5,5),np.uint8)
#Edge image dilation first parameter is the Canny Image second parameter is karnel size
#for messing with edge thickness other functions include cv2.erode
#img=cv2.dilate(img,kernel,iterations=1)

#cropping image
#img=img[0:100,150:300]

cv2.imshow("Image",img)
#cv2.rectangle(img,(100,100))

cv2.waitKey(0)




'''Loading video'''
# cap=cv2.VideoCapture(0)

# cap.set(10,100)

# while True:
#     success,img=cap.read()
#     cv2.imshow("video",img)
#     print(img)
#     if cv2.waitKey(1) and 0xFF == ord('q'):
#         break