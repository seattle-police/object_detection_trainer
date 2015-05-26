from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import os
import json
import re

def home(request):
    return render_to_response("home.html", {})
    
def get_coordinates(request):
    f = open('coordinates.json', 'r')
    #coordinates_json = json.loads(f.read())    
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
    options.num_threads = 2
    options.be_verbose = True


    training_xml_path = os.path.join("/home/azureuser/object_detection_trainer/", "training.xml")
    #testing_xml_path = os.path.join(faces_folder, "testing.xml")
    # This function does the actual training.  It will save the final detector to
    # detector.svm.  The input is an XML file that lists the images in the training
    # dataset and also contains the positions of the face boxes.  To create your
    # own XML files you can use the imglab tool which can be found in the
    # tools/imglab folder.  It is a simple graphical tool for labeling objects in
    # images with boxes.  To see how to use it read the tools/imglab/README.txt
    # file.  But for this example, we just use the training.xml file included with
    # dlib.
    dlib.train_simple_object_detector(training_xml_path, "detector.svm", options) 



    # Now that we have a face detector we can test it.  The first statement tests
    # it on the training data.  It will print(the precision, recall, and then)
    # average precision.
    #print("")  # Print blank line to create gap from previous output
    #print("Training accuracy: {}".format(
    #    dlib.test_simple_object_detector(training_xml_path, "detector.svm")))
    # However, to get an idea if it really worked without overfitting we need to
    # run it on images it wasn't trained on.  The next line does this.  Happily, we
    # see that the object detector works perfectly on the testing images.
    #print("Testing accuracy: {}".format(
    #    dlib.test_simple_object_detector(testing_xml_path, "detector.svm")))







    return HttpResponse('[]', content_type="application/json")

def get_frame_detections(requests, frame):
    import os
    import sys
    import glob

    import dlib
    from skimage import io
    detector = dlib.simple_object_detector("detector.svm")
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
    print frame
    img = io.imread('/datadrive/'+frame)
    print img
    dets = detector(img)
    print list(dets)
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
    #image = re.search('\d+_\d+\.png', image).group(0)
    #print request.POST['coordinates']
    for frame in frames:
        print frame
        frames[frame] = [[j.strip('px') for j in c if int(c[2].strip('px'))*int(c[3].strip('px'))*2 > 400] for c in frames[frame] if c]

    #coord_xml = ""
    #for coord in coordinates:
        
    #    coord_xml += "    <box top='%s' left='%s' width='%s' height='%s'/>\n" % (coord[0], coord[1], coord[2], coord[3])
    
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
    #coordinates_json[image] = coordinates
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
    #coord_xml = ""
    #for coord in coordinates:
        
    #    coord_xml += "    <box top='%s' left='%s' width='%s' height='%s'/>\n" % (coord[0], coord[1], coord[2], coord[3])
    
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