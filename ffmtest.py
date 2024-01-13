import os
import json
from string import ascii_lowercase as al

dir = os.path.join(os.getcwd(),"intermediary")
file = open(os.path.join(dir, os.listdir(dir)[0]))

info = json.load(file)

# Create and prepare inputs string
inputs = ""
for x in info:
  inputs = f"{inputs} -i {x['video_path']}"

filter = ""
number = 0
for x in info:
  if x['nen'] == 0:
    filter = f"{filter}[{number}]tpad=start_duration={x['delay']}ms[{al[number]}];"
  else:
    filter = f"{filter}[{number}]tpad=stop_duration={x['delay']}ms[{al[number]}];"
  number = number + 1

#print(filter)

command = f''' ffmpeg {inputs} \
               -filter_complex "{filter}[a][b][c]hstack=inputs=3" -s 1280x240 -r 30 test.mp4'''
               

#print(command) 
os.system(command)