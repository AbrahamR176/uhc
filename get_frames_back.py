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

vid1 = vid1[:-int(vid1[0][2])*20]
vid2 = vid2[:-int(vid2[0][2])*20]
vid1 = vid1[int(vid1[0][2])*20:]
vid2 = vid2[int(vid2[0][2])*20:]

differences = []
for x in vid1:
    for y in vid2:
        if x[3] == y[3]:
            diff = abs(x[0]-y[0])
            print(f"found match at: {x[0]}:{y[0]}, diff {diff}")
            if diff < 5000:
                differences.append(abs(x[0]-y[0]))

print(round(sum(differences)/len(differences)))

