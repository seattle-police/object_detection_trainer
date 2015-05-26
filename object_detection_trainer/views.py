from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import os
import json
import re
import multiprocessing 

def home(request):
    return render_to_response("home.html", {})
    
def get_coordinates(request):
    f = open('coordinates.json', 'r') 
    return HttpResponse(f.read(), content_type="application/json")
    
def train(request):
    import os
    import sys
    import glob

    import dlib
    from skimage import io


    
    faces_folder = '/home/azureuser/object_detection_trainer/media/'


    # Now let's do the training.  The train_simple_object_detector() function has a
    # bunch of options, all of which come with reasonable default values.  The next
    # few lines goes over some of these options.
    options = dlib.simple_object_detector_training_options()
    # Since faces are left/right symmetric we can tell the trainer to train a
    # symmetric detector.  This helps it get the most value out of the training
    # data.
    options.add_left_right_image_flips = True
    # The trainer is a kind of support vector machine and therefore has the usual
    # SVM C parameter.  In general, a bigger C encourages it to fit the training
    # data better but might lead to overfitting.  You must find the best C value
    # empirically by checking how well the trained detector works on a test set of
    # images you haven't trained on.  Don't just leave the value set at 5.  Try a
    # few different C values and see what works best for your data.
    options.C = 3
    # Tell the code how many CPU cores your computer has for the fastest training.
    options.num_threads = multiprocessing.cpu_count()
    options.be_verbose = True


    training_xml_path = os.path.join("/home/azureuser/object_detection_trainer/", "training.xml")
    dlib.train_simple_object_detector(training_xml_path, "detector.svm", options) 

    return HttpResponse('{"status": "completed"}', content_type="application/json")

def get_frame_detections(requests, frame):
    import os
    import sys
    import glob

    import dlib
    from skimage import io
    detector = dlib.simple_object_detector("detector.svm")
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
    return HttpResponse(json.dumps(detections), content_type="application/json")
    
    
def get_detections(request):
    cmd = "/home/azureuser/dlib-18.14/examples/build/test_detection /home/azureuser/dlib-18.14/examples/faces2/faces/"
    detections_output = os.popen(cmd).read().strip()
    detections = dict([(i, []) for i in range(1, 62)])
    print detections_output
    for line in detections_output.split('\n'):
        m = re.search('(?P<i>\d+)\s+\[\((?P<x1>\d+), (?P<y1>\d+)\)\s+\((?P<x2>\d+), (?P<y2>\d+)\)\]', line)
        print m
        if m:
            x1 = int(round(int(m.group('x1')) / float(2)))
            x2 = int(round(int(m.group('x2')) / float(2)))
            y1 = int(round(int(m.group('y1')) / float(2)))
            y2 = int(round(int(m.group('y2')) / float(2)))
            w = x2 - x1
            h = y2 - y1
            try:
                detections[int(m.group('i'))].append((x1, y1, w, h))
            except:
                print 'problem with', i
            
    return HttpResponse(json.dumps(detections), content_type="application/json")
    
def generate_xml(coordinates_dict):
    # sort it
    coordinates_dict = sorted(coordinates_dict.items(), key=lambda x: x[0])
    xml = """
    <?xml version='1.0' encoding='ISO-8859-1'?> <?xml-stylesheet type='text/xsl' href='image_metadata_stylesheet.xsl'?> 
<dataset> <name>Training faces</name> <images>
    """
    for item in coordinates_dict:
        coord_xml = ""
        for coord in item[1]:
            print coord
            if coord:
                coord_xml += "    <box top='%s' left='%s' width='%s' height='%s'/>\n" % (coord[0], coord[1], coord[2], coord[3])
        s = """\n  <image file='/datadrive/%s'>
    %s
      </image>\n""" % (item[0], coord_xml.strip('\n'))
        xml += s
    xml += """
</images>
</dataset>    
    """
    return xml

def add_all_to_training(request):
    frames = json.loads(request.POST['frames'])
    frames = dict([(re.search('\d+_\d+\.png', item[0]).group(0), item[1]) for item in frames.items()])
    for frame in frames:
        print frame
        frames[frame] = [[j.strip('px') for j in c if int(c[2].strip('px'))*int(c[3].strip('px'))*2 > 400] for c in frames[frame] if c]

    
    try:
        f = open('coordinates.json', 'r')
        coordinates_json = json.loads(f.read())
        if not coordinates_json:
            coordinates_json = {}
        f.close()
    except:
        f = open('coordinates.json', 'w')
        f.write('{}')
        f.close()
        coordinates_json = {}
    print coordinates_json
    coordinates_json.update(frames)
    f = open('coordinates.json', 'w')
    f.write(json.dumps(coordinates_json))    
    
    
    xml = generate_xml(coordinates_json)
    print xml
    f = open('training.xml', 'w')
    f.write(xml)
    f.close()
    return HttpResponse('')
    
def add_to_training(request):
    image = request.POST['image']
    image = re.search('\d+_\d+\.png', image).group(0)
    print request.POST['coordinates']
    coordinates = [[j.strip('px') for j in c if int(c[2].strip('px'))*int(c[3].strip('px'))*2 > 400] for c in json.loads(request.POST['coordinates'])]
    
    try:
        f = open('coordinates.json', 'r')
        coordinates_json = json.loads(f.read())
        f.close()
    except:
        f = open('coordinates.json', 'w')
        f.write('{}')
        f.close()
        coordinates_json = {}
    coordinates_json[image] = coordinates
    f = open('coordinates.json', 'w')
    f.write(json.dumps(coordinates_json))    
    
    
    xml = generate_xml(coordinates_json)
    print xml
    f = open('training.xml', 'w')
    f.write(xml)
    f.close()
    return HttpResponse('')
