import os
import sys
from object_detection_trainer import settings
from_folder = sys.argv[1]
to_folder = settings.FRAMES_DIR
if not (to_folder[-1] in ['/', '\\']):
    to_folder = to_folder + '/'

videos = sorted(os.listdir(from_folder))
for i, video in enumerate(videos):
    os.system('ffmpeg -threads 0 -i "%s%s" "%s%s_%%6d.png"' % (from_folder, video, to_folder, i))
