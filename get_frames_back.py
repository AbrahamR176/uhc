import pickle
import os
import math
import copy
import json
import time

# Create primary default values
vids = []
files = os.listdir("times")
folder = os.path.join(os.getcwd(),"times")
infos = []

# Prepares the path of the intermediary files for ease of reading
for x in range(len(files)):
    files[x] = os.path.join(folder, files[x])

# Read intermediate files
for x in range(len(files)):
    vids.append([])
    with open(f"{os.path.join(folder,str(x))}", 'rb') as f:
        infos.append(pickle.load(f))
        while True:
            try:
                vids[x].append(pickle.load(f))
            except EOFError:
                break

# initialize useful values
differences = []
included = []
baseline = 1
target_fps = vids[baseline][0][2]

# fix non-30fps videos
for x in vids:
    if x[0][2] != 30:
        for y in range(len(x)):
            x[y][0] = x[y][0] + (y+1)*(target_fps-x[y][2])

# Get differences between baseline video and rest
for z in vids:
    temp = []
    if z != vids[baseline]: 
        for x in vids[baseline]:
            for y in z:
                if x[3] != "None" and y[3] != "None":
                    if len(x[3]) == 4 and len(y[3]) == 4:
                        if int(x[3]) != 3000:
                            if int(x[3]) == int(y[3]):   
                                if int(x[3]) not in included:
                                    included.append(int(x[3]))
                                    print(f"got a match at {x[0]}:{y[0]}, time: {x[3]},{y[3]}, {x[0] - y[0]}")
                                    temp.append(((x[0] - y[0])))

    differences.append(copy.deepcopy(temp))
    included = []

# Get the mode of each video in differences, for use as errors
errors = []
for x in differences:
    try:
        errors.append(max(set(x), key=x.count))
    except:
        errors.append([])

# Fix out of scope/erroneous values
for x in range(len(differences)):
    if x != baseline:
        for y in range(len(differences[x])):
            if differences[x][y] > errors[x] + vids[x][0][2] * 2 or differences[x][y] < errors[x] - vids[x][0][2] * 2 :
                differences[x][y] = errors[x]

# get averages in differences in ms
mss = []
for x in range(len(differences)):
    if x != baseline:
        mss.append(round(((sum(differences[x])/len(differences[x]))/vids[x][0][2])*1000))
    else:
        mss.append(0)

dir = os.path.join(os.getcwd(),"intermediary")
if not os.path.exists(dir):
    os.mkdir(dir)
else:
    for file in os.listdir(dir):
        os.remove(os.path.join(dir,file))

results = open(os.path.join(dir, str(time.time()) + ".json"), "a")

result = []
for x in range(len(vids)):
    temp = dict(video_path   = infos[x][0],
                region       = infos[x][1],
                data_path    = infos[x][2],
                frame_target = infos[x][3],
                delay        = abs(mss[x]),
                nen          = 0)
    if mss[x] < 0: temp['nen'] = 1
    result.append(temp)
    
json.dump(result, results, indent=4)
    
