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
for x in vid1:
    for y in vid2:
        if x[3] == y[3]:
            diff = abs(x[0]-y[0])
            if diff < 5000:
                print(f"found match at: {x[0]}:{y[0]}, diff {diff}")
                differences.append(diff)

old = 0
most = 0
counter = 0
hicounter = 0
for x in differences:
    if old == x:
        most = x
        counter = counter + 1
    else:
        if counter > hicounter:
            hicounter = counter
        counter = 0
    old = x

print(most, hicounter)