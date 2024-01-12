import pickle
import os
import math
import copy

vids = []

files = os.listdir("times")
folder = os.path.join(os.getcwd(),"times")

for x in range(len(files)):
    files[x] = os.path.join(folder, files[x])

for x in range(len(files)):
    vids.append([])
    with open(f"{os.path.join(folder,str(x))}", 'rb') as f:
        while True:
            try:
                vids[x].append(pickle.load(f))
            except EOFError:
                break

differences = []
included = []

baseline = 1

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
                                    temp.append(abs(x[0] - y[0]))
                                    print(f"got a match at {x[0]}:{y[0]}, time: {x[3]},{y[3]}, {x[0] - y[0]}")
    differences.append(copy.deepcopy(temp))
    included = []
            
print(differences)
#error = max(set(differences), key=differences.count)
#for x in range(len(differences)):
#    if differences[x] > error + vids[x][0][2] or differences[x] < error - vids[x][0][2]:
#        differences[x] = error

#print(round(((sum(differences)/len(differences))/30)*1000))

