import os

path1 = "C:\\Users\\abraham\\Documents\\Code\\uhc\\vid5.mp4"
path2 = "C:\\Users\\abraham\\Documents\\Code\\uhc\\vid6.mp4"
d=1107

command = f'ffmpeg -i {path1} -i {path2}' \
          f' -filter_complex "[1]tpad=start_duration=36.9[a];[0][a]hstack"' \
          f' -s 1280x360 -r 30 test.mp4'

#print(command)
os.system(command)