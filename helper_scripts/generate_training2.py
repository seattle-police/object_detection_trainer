import os
import json

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
            #print coord
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
    
f = open('coordinates.json', 'r')
coordinates = json.loads(f.read())
f.close()
new_coordinates = {}
for coord in coordinates.items():
    #print coord[0]
    good = True
    if not coord[1]:
        good = False
    for c in coord[1]:
    
        if c:
            #print c, coord[0]
            #ratios.append(float(c[2])/float(c[3]))
            ratio = float(c[2])/float(c[3])
            #if ratio < .9 or ratio > 1.1:
            #    good = False
                #print coord[0], float(c[2])/float(c[3])
        else:
            good = False
            print coord[1]
    if good:
        new_coordinates[coord[0]] = coord[1]    
f = open('training2.xml', 'w')
f.write(generate_xml(new_coordinates))
f.close()