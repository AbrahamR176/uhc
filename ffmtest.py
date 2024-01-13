import os
import json

dir = os.path.join(os.getcwd(),"intermediary")
file = open(os.path.join(dir, os.listdir(dir)[0]))

info = json.load(file)

command = f''' ffmpeg -i "{info[2]['video_path']}" -i "{info[1]['video_path']}" -i "{info[0]['video_path']}" \
               -filter_complex \
                "[1]tpad=start_duration={info[1]['delay']}ms[a];\
                 [2]tpad=start_duration={info[0]['delay']}ms[b];\
                 [0][a][b]hstack=inputs=3"' \
               -s 3840x720 -r 30 test.mp4'''

#print(command)
os.system(command)