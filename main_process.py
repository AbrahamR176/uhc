import os
import cv2
import json
from video_processor import obtain_video_data
from get_frames_back import obtain_intermediary_file

def main():

    # Ensure all the folders are created
    prepare_folders()

    # initialize primary functions
    input_folder = os.path.join(os.getcwd(), "input")
    info_file_path = os.path.join(input_folder, "details.json")

    # Placeholder values
    rois = []
    details = []
    players = []
    decision = "y"
    n_episodes = 0

    # Get the folders inside of the input folder, and format them for comp
    targets = os.listdir(input_folder)
    for x in range(len((targets))):
        if ".json" in targets[x]:
            targets.remove(targets[x])
        else:
            targets[x] = os.path.join(input_folder, targets[x])

    # Get the number of episodes
    for x in targets:
        if len(os.listdir(x)) > n_episodes:
            n_episodes = len(os.listdir(x))

    # Get the player names:
    for x in targets:
        players.append(os.path.basename(x))

    # Skip details obtaining if previosly gotten
    if os.path.exists(info_file_path):
        decision = input("Details.json file already exists, do you wish to recreate it? (y-N): ")
        if decision.lower() != 'y' and decision.lower() != 'n':
            decision = "n"
        
    # Get the regions for all of the inputs
    if decision == "y":
        for x in targets:
            roi= get_region(os.path.join(x, os.listdir(x)[0]))
            rois.append(roi)

        for x in range(n_episodes):
            temp = []
            for y in range(len(targets)):
                try:
                    temp.append(dict(
                        video_path = (os.path.join(targets[y],
                                     (os.listdir(targets[y])[x]))),
                        file = str(x+1) + " - " + players[y] + ".data",
                        roi = rois[y]))
                except:
                    temp.append(dict(
                        video_path = "none",
                        file = "none",
                        roi = 0))

            details.append(temp)
                
        info_file = open(info_file_path, "w")
        json.dump(details, info_file, indent=4)

    # Retrieve all the information from the json file
    info_file = open(info_file_path, "r")    
    details = json.load(info_file)

    # Skip details obtaining if previosly gotten
    if os.path.exists(info_file_path):
        decision = input("This step can take a long time, are you sure you want to create video data? (y-N): ")
        if decision.lower() != 'y' and decision.lower() != 'n':
            decision = "n"

    # Queue all the data to process into the output files
    if decision == 'y':
        # do the rest of the calculation
        for x in range(len(details)):
            obtain_video_data(details[x], x+1)

    #obtain_intermediary_file(os.path.join(os.path.join(os.getcwd(), "episodes"), "1"), 
    #                         os.path.join(os.path.join(os.getcwd(), "episodes")))

def prepare_folders(input_f="input", episodes_f="episodes", log_f="logs"):
    root = os.getcwd()

    if not os.path.exists(os.path.join(root,input_f)):
        os.mkdir(os.path.join(root, input_f))

    if not os.path.exists(os.path.join(root,episodes_f)):
        os.mkdir(os.path.join(root, episodes_f))

    if not os.path.exists(os.path.join(root,episodes_f)):
        os.mkdir(os.path.join(root, log_f))

def get_region(path):
    print(path)
    im = cv2.VideoCapture(path)
    im.set(1,15000)
    s, i = im.read()
    r = cv2.selectROI(i)
    return r

if __name__ == "__main__":
    main()