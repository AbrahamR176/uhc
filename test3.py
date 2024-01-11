#This file will use image similarities to see if the required sync can be achieved

from PIL import Image
import imagehash
import cv2
from numpy import array
import threading
import math

path1 = "C:\\Users\\abraham\\Documents\\Code\\uhc\\vid2.mp4"
path2 = "C:\\Users\\abraham\\Documents\\Code\\uhc\\vid4.mp4"
vid1 = cv2.VideoCapture(path1)
vid2 = cv2.VideoCapture(path2)

vid1.set(1,34433)
s1, result1 = vid1.read() 

vid2.set(1,34433)
s2, result2 = vid2.read() 

#r1 = cv2.selectROI(result1)
#r2 = cv2.selectROI(result2)

result1 = cv2.cvtColor(result1, cv2.COLOR_BGR2HSV)
result1 = cv2.inRange(result1, array([0, 0, 250]), array([255, 255, 255]))
result1 = result1[int(result1.shape[0]/2):int(result1.shape[0]), 0:int(result1.shape[1]/2)] 
cv2.selectROI(result1)

hash0 = imagehash.average_hash(Image.fromarray(result1))

total = 1
lowest = 1000
target = 0

success, result2 = vid2.read()
print("starting img process...")
while(success):
    result2 = cv2.cvtColor(result2, cv2.COLOR_BGR2HSV)
    result2 = cv2.inRange(result2, array([0, 0, 250]), array([255, 255, 255]))
    result2 = result2[int(result2.shape[0]/2):int(result2.shape[0]), 0:int(result2.shape[1]/2)]
    
    #hash method
    hash1 = imagehash.average_hash(Image.fromarray(result2))
    if hash0-hash1 < lowest:
        lowest = hash0-hash1
        target = total

    #template matching
    #con = cv2.matchTemplate(result2, result1,cv2.TM_CCOEFF_NORMED).max()
    #if highest < con:
    #    highest = con
    #    target = total
    cv2.imwrite(f"result\\{total}.png",result2)
    vid2.set(1,total+30)
    success, result2 = vid2.read()
    total = total + 30


vid2.set(1,target)
s1, result2 = vid2.read() 
cv2.selectROI("The game", result2)
