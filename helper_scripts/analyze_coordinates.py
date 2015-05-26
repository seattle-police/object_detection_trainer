import os
import json

f = open('coordinates.json')
coordinates = json.loads(f.read())
ratios = []
for coord in coordinates.items():
    #print coord[0]
    for c in coord[1]:
        if c:
            #print c, coord[0]
            ratios.append(float(c[2])/float(c[3]))
            if float(c[2])/float(c[3]) < .7:
                print coord[0], float(c[2])/float(c[3])
print 'average', sum(ratios)/len(ratios)
                
