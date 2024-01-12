import os

command = f"ffmpeg -i input/kaky.mp4 -filter:v fps=fps=30 kaky30.mp4"

os.system(command)