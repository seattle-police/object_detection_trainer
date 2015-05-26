import os
import sys
import glob

import dlib
from skimage import io
print 'before'
detector = dlib.simple_object_detector("detector.svm")
print 'after'
#io.imsave('detector.png', detector)
# We can look at the HOG filter we learned.  It should look like a face.  Neat!
#win_det = dlib.image_window()
#win_det.set_image(detector)

# Now let's run the detector over the images in the faces folder and display the
# results.
# print("Showing detections on the images in the faces folder...")
#win = dlib.image_window()
#s = ''
#files = sorted([image for image in os.listdir('media') if image.endswith('.jpg')])[:200]
#detections = dict([(i, []) for i in range(1, len(files)+1)])
#for i, f in enumerate(files):
#    print "Processing file: {}\n".format(f)
def detect(frame):
    #print frame
    img = io.imread('/datadrive/'+frame)
    #print img
    #print 'before %s' % (frame)
    dets = detector(img)
    #print 'after %s' % (frame)
    #print list(dets)
    #s += "Number of faces detected: {}\n".format(len(dets))
    detections = []
    for k, d in enumerate(dets):
        #s += "Detection {}: Left: {} Top: {} Right: {} Bottom: {}\n".format(k, d.left(), d.top(), d.right(), d.bottom())
        #x1 = int(round(int(d.left()) / float(2)))
        #x2 = int(round(int(d.right()) / float(2)))
        #y1 = int(round(int(d.top()) / float(2)))
        #y2 = int(round(int(d.bottom()) / float(2)))
        x1 = d.left()
        x2 = d.right()
        y1 = d.top()
        y2 = d.bottom()
        w = x2 - x1
        h = y2 - y1
        detections.append((x1, y1, w, h))   
    if detections:
        print detections
    print frame
    return (frame, detections)    
    


from joblib import Parallel, delayed  
import multiprocessing

inputs = ['0_%05d.png' % (i) for i in range(5001, 5500)] 
#def processInput(i):  
#    return i * i

num_cores = multiprocessing.cpu_count()

print("numCores = " + str(num_cores))

results = Parallel(n_jobs=num_cores)(delayed(detect)(frame) for frame in inputs)  

print(results)
print 'missed', [len(item[1]) for item in results].count(0)
import json
f = open('results.json', 'w')
f.write(json.dumps(dict(results)))
f.close()
