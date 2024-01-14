import time
import numpy as np
from multiprocessing.pool import ThreadPool
import os
import pickle
import platform
import pytesseract as pt 
import cv2
import re

def obtain_video_data(info, no_episode):

    # Initialize useful values
    vids = []
    rois = []
    names = []

    # prepare the path for the results
    result_path = prepare_dic(os.path.join((os.path.join(os.getcwd(), "episodes")), str(no_episode)))

    # get the paths for the files
    for x in info:   
        vids.append(x['video_path'])
        rois.append(x['roi'])
        names.append(x['file'])

    # create and start the threads to process the times for the videos
    threads = []
    for x in range(len(info)):
        thread = ThreadPool(processes=1)
        tt1 = thread.apply_async(process_vid, 
                                (vids[x], 
                                rois[x], 
                                os.path.join(result_path, names[x])))
        threads.append(tt1)

    # get the data form all the threads
    for x in threads:
        x.get()

    # return a satisfactory answer
    return 1

def get_paths(path):

    # get all the files inside of the intest folder
    files = os.listdir(os.path.join(os.getcwd(), path))
    folder = os.path.join(os.getcwd(), path)

    for x in range(len(files)):
        files[x] = os.path.join(folder, files[x])
        files[x] = files[x][:-4]
    return files

def process_vid(vid_path, r, path):

    # Setting the path for pytesseracts executable on windows
    if platform.system() == "Windows":
        pt.pytesseract.tesseract_cmd = 'C:\\Users\\abraham\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

    # Open file in append mode
    if os.path.exists(path):
        os.remove(path)
    file = open(path, "ab")

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

        print(f"{total:.0f} {os.path.split(vid_path)[len(os.path.split(vid_path)) - 2]}")
        frame = prep_frame(image, r)
        msg = pt.image_to_string(frame, lang="mc") 

        # Leave this part of the code if only numbers matter
        msg = re.sub("[^0-9]+","",msg)

        if msg != "":
            pickle.dump([total, int(frame_cnt), frame_target, msg], file)
        else:
            pickle.dump([total, int(frame_cnt), frame_target, "None"], file)

    # finish timer to get final process time
    file.close()
    return 1

def prep_frame(result: np.ndarray, r):

    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    result = result[int(r[1]):int(r[1]+r[3]),  
                    int(r[0]):int(r[0]+r[2])] 
    result = cv2.resize(result, None, fx=3, fy=3)
    sharpen_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    result = cv2.filter2D(result, -1, sharpen_filter)
    return result

def prepare_dic(target="data"):

    # Prepares the directory that will be used for the program
    path = target

    # Make sure the folder is created
    if not os.path.exists(path):
        os.mkdir(path)
    return path
