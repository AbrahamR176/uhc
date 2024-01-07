import pytesseract as pt 
import cv2
import os
import numpy as np
from numpy import array

pt.pytesseract.tesseract_cmd = 'C:\\Users\\abraham\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'
GTK_FOLDER = "C:\\Program Files\\GTK3-Runtime Win64\\bin"
os.environ['PATH'] = GTK_FOLDER + os.pathsep + os.environ.get('PATH', '')

path = "C:\\Users\\abraham\\Documents\\Code\\uhc\\vid2.mp4"
model_path = "C:\\Program Files\\Tesseract-OCR\\tessdata\\mc.traineddata"
vid = cv2.VideoCapture(path)

vid.set(1,4931)
s, result = vid.read() 

result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
#result = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
#result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
result = result[646:664,13:460]
result = cv2.resize(result, None, fx=3, fy=3)
#result = cv2.inRange(result, array([0, 0, 135]), array([255, 255, 255]))
#result = cv2.inRange(result, array([0, 0, 150]), array([255, 255, 255]))
#result = cv2.adaptiveThreshold(cv2.GaussianBlur(result, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
#result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
#result = cv2.threshold(result, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

sharpen_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
result = cv2.filter2D(result, -1, sharpen_filter)
#result = cv2.medianBlur(result, 1)


print(pt.image_to_string(result, lang="mc"))

cv2.imwrite("output.png", result)