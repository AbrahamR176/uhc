import pytesseract as pt 
import cv2
import time
import numpy as np
from numpy import array
import easyocr

pt.pytesseract.tesseract_cmd = 'C:\\Users\\abraham\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

path = "C:\\Users\\abraham\\Documents\\Code\\uhc\\vid2.mp4"
vid = cv2.VideoCapture(path)

for x in range(4032):
    success, image = vid.read()

result = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
result = result[630:680,0:460]
result = cv2.resize(result, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
result = cv2.inRange(result, array([0, 0, 135]), array([255, 255, 255]))
#result = cv2.inRange(result, array([0, 0, 150]), array([255, 255, 255]))
#result = cv2.adaptiveThreshold(cv2.GaussianBlur(result, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
#result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
#result = cv2.threshold(result, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
reader = easyocr.Reader(gpu=False,lang_list=['es','en'])
print(pt.image_to_string(result))
print(reader.readtext(image=result))

cv2.imwrite("output.png", result)