import os
videos = sorted(os.listdir('/home/azureuser/Dropbox/Public/Spokane Police/'))
for i, video in enumerate(videos):
    os.system('ffmpeg -threads 0 -i "/home/azureuser/Dropbox/Public/Spokane Police/%s" "/datadrive/%s_%%5d.png"' % (video, i))
