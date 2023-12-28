import pytesseract as pt 
import cv2
import time
import numpy as np
from numpy import array
import easyocr

pt.pytesseract.tesseract_cmd = 'C:\\Users\\abraham\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

def main():
    path = "C:\\Users\\abraham\\Documents\\Code\\uhc\\vid2.mp4"
    process_vid(path)

def process_vid(vid_path, frame_target=30):
    #start timer
    start = time.time()

    #start video instance and get the first frame
    im = cv2.VideoCapture(vid_path)
    frames = im.get(cv2.CAP_PROP_FRAME_COUNT)
    success,image = im.read()
    reader = easyocr.Reader(gpu=False,lang_list=['es','en'], verbose=False)

    #counter
    counter = 1
    total = 1

    while(success):
        # get the next frame
        success, image = im.read()

        #for every "frame_target" #, do work on the frame
        if counter == frame_target:
            frame = prep_frame(image, total)
            msg = reader.readtext(image=frame)
            if msg != "":
                print(f"Frame: {total} of {frames}, text: {msg}")
            counter = 1
        else:
            pass

        # update targets
        counter = counter + 1
        total = total + 1

    # finish timer to get final process time
    end = time.time()
    print((end-start)*1)

def prep_frame(frame: any, number):

    result = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    result = result[630:680,0:460]
    result = cv2.resize(result, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    result = cv2.inRange(result, array([0, 0, 135]), array([255, 255, 255]))

    cv2.imwrite(f"result\\{number}.png",result)
    return result

if __name__ == '__main__':
    main()
