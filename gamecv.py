import cv2
import pygame
import math
import numpy as np
import random
import sys


HEIGHT=600
WIDTH=900


win=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.init()

cap=cv2.VideoCapture(0)

while True:
    success,img=cap.read()
    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img=cv2.resize(img,(300,300))
    img=cv2.Canny(img,150,150)
    cv2.imshow("video",img)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

pygame.quit()
