import os

path1 = f"{os.getcwd()}/vid5.mp4"
path2 = f"{os.getcwd()}/vid7.mp4"
d=1107

command = f'ffmpeg -i {path1} -i {path2}' \
          f' -filter_complex "[1]tpad=start_duration=22289ms[a];[0][a]hstack"' \
          f' -s 720x180 -r 30 test.mp4'

#print(command)
os.system(command)