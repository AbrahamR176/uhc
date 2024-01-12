import pickle
import os
import math

vid1 = []
vid2 = []

with open(f"{os.getcwd()}\\times\\vid5.txt", 'rb') as f:
    while True:
        try:
            vid1.append(pickle.load(f))
        except EOFError:
            break

with open(f"{os.getcwd()}\\times\\vid6.txt", 'rb') as f:
    while True:
        try:
            vid2.append(pickle.load(f))
        except EOFError:
            break

differences = []
included = []
for x in vid1:
    for y in vid2:
        if x[3] != "None" and y[3] != "None":
            if len(x[3]) == 4 and len(y[3]) == 4:
                if int(x[3]) != 3000:
                    if int(x[3]) == int(y[3]):   
                        if int(x[3]) not in included:
                            included.append(int(x[3]))
                            differences.append(abs(x[0] - y[0]))
                            print(f"got a match at {x[0]}:{y[0]}, time: {x[3]},{y[3]}, {x[0] - y[0]}")

error = max(set(differences), key=differences.count)
for x in differences:
    if x > error + vid1[0][2] and x < error - vid1[0][2]:
        x = error

print(sum(differences)/len(differences))

