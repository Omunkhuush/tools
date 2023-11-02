
from pandas import DataFrame
from xml.etree import ElementTree as ET
from os import listdir
from os.path import isfile, join
import cv2

classes = ['Bus', 'Bike', 'Car', 'Pedestrian', 'Truck']

annotationPath = "../newImages/annotations/"
imagePath = '../newImages/images/'
labelSavePath = '../newImages/labels/'

xmlfiles = [f for f in listdir(annotationPath) if join(annotationPath, f)]
objects = []

for i in xmlfiles:
    print(i)
    tree = ET.parse(annotationPath+i)
    name = i.split(".")[0]
    txt = name + ".txt"
    imageName = name+".png"
    img = cv2.imread(imagePath+imageName)
    height, width, c = img.shape
    f = open(labelSavePath+txt, "w")
    for obj in tree.findall('object'):
        obj_struct = {}
        classs = (obj.find('name').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        b2box = DataFrame(obj_struct).to_numpy()
        k = classes.index(classs)
        xmin = b2box[0][0]
        ymin = b2box[1][0]
        xmax = b2box[2][0]
        ymax = b2box[3][0]
        x = ((xmin+xmax)/2)/width
        y = ((ymin+ymax)/2)/height
        wh = (xmax-xmin)/width
        he = (ymax-ymin)/height
        f.write(str(k)+" "+str(x)+" "+str(y)+" "+str(wh)+" "+str(he)+"\n")
    f.close()
print("done")
