import os
import sys
import glob

import dlib
from skimage import io

detector = dlib.simple_object_detector("../detector.svm")

def detect(frame):
    img = io.imread('/datadrive/'+frame)
    dets = detector(img)
    detections = []
    for k, d in enumerate(dets):
        x1 = d.left()
        x2 = d.right()
        y1 = d.top()
        y2 = d.bottom()
        w = x2 - x1
        h = y2 - y1
        detections.append((x1, y1, w, h))   
    return (frame, detections)    
    


from joblib import Parallel, delayed  
import multiprocessing

inputs = ['0_%05d.png' % (i) for i in range(5001, 5500)] 

num_cores = multiprocessing.cpu_count()

print("numCores = " + str(num_cores))

results = Parallel(n_jobs=num_cores)(delayed(detect)(frame) for frame in inputs)  

print(results)
print 'missed', [len(item[1]) for item in results].count(0)
import json
f = open('results.json', 'w')
f.write(json.dumps(dict(results)))
f.close()
