import numpy as np
import cv2
from os import listdir
from os.path import isfile, join
import os.path

import json

path = '/home/munkhuush/Desktop/projects/asphalt_data/'

jsons = [file for file in os.listdir(path) if file.endswith('.json')]

classes = ['white line', 'yellow line']
for i in jsons:
    txtName = i.split(".")[0]+'.txt'
    print(i,'----->',txtName)
    f = open(path+i)
    data = json.load(f)

    imgWidth = data['imageWidth']
    imgHeight = data['imageHeight']

    ff = open(path+txtName,'w')

    for dt in data['shapes']:    
        className = dt['label']
        points = dt['points']
        label = []
        classId = classes.index(className)
        for pt in points:
            x,y = pt
            x = x/imgWidth
            y = y/imgHeight
            label.append(x)
            label.append(y)
        listToStr = ' '.join([str(elem) for elem in label])
        ff.write(str(classId)+" "+listToStr+"\n")
    ff.close()