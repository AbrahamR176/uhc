import os
import json
from string import ascii_lowercase as al
import math

dir = os.path.join(os.getcwd(),"intermediary")
file = open(os.path.join(dir, os.listdir(dir)[0]))
info = json.load(file)

# Create and prepare inputs string
inputs = ""
for x in info:
  inputs = f"{inputs} -i \"{x['video_path']}\""

# Fix timings
for x in info:
   x_delay = x['delay']
   for y in info:
      y['delay'] = y['delay'] + abs(x_delay)

lowest = math.inf
for x in info:
   if x['delay'] < lowest:
      lowest = x['delay']

for x in info:
   x['delay'] = x['delay'] - lowest

# Calculate the rows and columns for the final result
columns = math.ceil(math.sqrt(len(info)))
rows = math.ceil(len(info)/columns)
print(f"colums: {columns}, rows: {rows}")

# Create the complex filter used for adding the dalays
filter = ""
number = 0
for x in range(rows*columns):
    if x < len(info):
        filter = f"{filter}[{number}]tpad=start_duration={info[x]['delay']}ms[{al[number]}]; "
    else:
        filter = f"{filter}color=black:1280x720[{al[number]}]; "
    number = number + 1

# Create the complex positioning filter for the videos
stacks = ""
position = 0
layers = []
for x in range(rows):
    for y in range(columns):
        stacks = f"{stacks}[{al[position]}]"
        position = position + 1
    stacks = f"{stacks}hstack=inputs={columns}[{al[columns*x:columns+(x*columns)]}]; "
    layers.append(al[columns*x:columns+(x*columns)])
for x in range(len(layers)):
   stacks = f"{stacks}[{layers[x]}]"
stacks = f"{stacks}vstack=inputs={rows}"

command = f''' ffmpeg {inputs} \
    -filter_complex "{filter}{stacks}" \
    -s 320x180 -r 30 -af "adelay={info[0]['delay']}|{info[0]['delay']}" \
    test.mkv'''
               
print(command) 
os.system(command)
    
