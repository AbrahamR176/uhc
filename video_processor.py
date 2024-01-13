import pytesseract as pt 
import cv2
import time
import numpy as np
from multiprocessing.pool import ThreadPool
import os
import pickle
import re

#pt.pytesseract.tesseract_cmd = 'C:\\Users\\abraham\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

def main():

    # prepare the path for the results
    result_path = prepare_dic("times")

    paths = get_paths("input")
    print(paths)
    # get the region for the videos where the matching content is

    regions = []
    for x in paths:
        regions.append(get_region(x))

    # create and start the threads to process the times for the videos

    threads = []
    for x in range(len(regions)):
        thread = ThreadPool(processes=1)
        tt1 = thread.apply_async(process_vid, (paths[x], regions[x], os.path.join(result_path, str(x))))
        threads.append(tt1)

    for x in threads:
        x.get()

    return 1

def get_paths(path):
    files = os.listdir(os.path.join(os.getcwd(), path))
    folder = os.path.join(os.getcwd(),path)

    for x in range(len(files)):
        files[x] = os.path.join(folder, files[x])
    return files

def write_result(result_list, dir, name):
    file = open(f"{dir}\name.txt", "w")

    for x in result_list:
        pass

def process_vid(vid_path, r, path, frame_target=1000):

    # Open file in append mode
    if os.path.exists(path):
        os.remove(path)
    file = open(path, "ab")

    #start timer
    start = time.time()

    #start video instance and get the first frame
    im = cv2.VideoCapture(vid_path)

    # Get neccessary processing information
    frame_target = im.get(cv2.CAP_PROP_FPS)
    frame_cnt = im.get(cv2.CAP_PROP_FRAME_COUNT)

    # Set proper frame
    im.set(1,0)
    success = True
    total = 0

    # Write identifying information in the beginning of the file
    info = [vid_path, r, path, frame_target]
    pickle.dump(info, file)

    while(success):
        # Get the next frame
        if total + frame_target < frame_cnt:
            im.set(1, total+frame_target)
            success, image = im.read()
            total = total + frame_target
        else:
            break

        print(f"processing {total}")
        frame = prep_frame(image, total, r)
        msg = pt.image_to_string(frame, lang="mc") 

        # Leave this part of the code if only numbers matter
        msg = re.sub("[^0-9]+","",msg)

        if msg != "":
            fancy_write(file, [total, int(frame_cnt), frame_target, msg])
        else:
            fancy_write(file, [total, int(frame_cnt), frame_target, "None"])

    # finish timer to get final process time
    end = time.time()
    print((end-start)*1)
    file.close()
    return 1

def timer_target(msg):
    if len(msg) == 5:
        msg[2] = ""
    return msg

def fancy_write(file, info):
    pickle.dump(info, file)

def prep_frame(result: np.ndarray, number, r):

    #1.1
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    result = result[int(r[1]):int(r[1]+r[3]),  
                    int(r[0]):int(r[0]+r[2])] 
    result = cv2.resize(result, None, fx=3, fy=3)
    sharpen_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    result = cv2.filter2D(result, -1, sharpen_filter)
    return result

def get_region(path):
    im = cv2.VideoCapture(path)
    im.set(1,30000)
    s, i = im.read()
    r = cv2.selectROI(i)
    return r

def prepare_dic(target="times"):
    path = f"{os.path.join(os.getcwd(), target)}"
    if not os.path.exists(path):
        print("Creating directory")
        os.mkdir(path)
        return path
    else:
        print("path already created")
        return path

if __name__ == '__main__':
    main()
