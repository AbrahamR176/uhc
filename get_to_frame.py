import os
import cv2

#frame = 66120:64994

path1 = "C:\\Users\\abraham\\Documents\\Code\\uhc\\vid5.mp4"
path2 = "C:\\Users\\abraham\\Documents\\Code\\uhc\\vid7.mp4"

im1 = cv2.VideoCapture(path1)
im2 = cv2.VideoCapture(path2)

im1.set(1, 35695)
s, i1 = im1.read()

im2.set(1, 35000)
s, i2 = im2.read()

cv2.selectROI(i1)
cv2.selectROI(i2)
