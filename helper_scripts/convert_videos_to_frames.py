import os
import sys

from_folder = sys.argv[1]
to_folder = sys.argv[2]

videos = sorted(os.listdir(from_folder))
for i, video in enumerate(videos):
    os.system('ffmpeg -threads 0 -i "%s%s" "/datadrive/%s_%%6d.png"' % (from_folder, video, to_folder, i))
