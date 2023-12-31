# -*- coding: utf-8 -*-

import os 
import numpy
from pandas import DataFrame
from xml.etree import ElementTree as ET
import cv2 as cv
from os import listdir
from os.path import isfile, join

imagesPath = "../fisheye_6class/Data/images/"
annotationsPath = '../fisheye_6class/Data/annotations/'
min_area = 1024 #784 #1024 18x18 28x28 32x32 
max_area = 9216 #32400 #180x180 25600 160x160 65536 #256x256
def convert(xmin,ymin,xmax,ymax):
    #dw = 1./(size[0]) # 1/400
    #dh = 1./(size[1]) # 1/400
    #x = (box[0] + box[1])/2.0 - 1   
    #y = (box[2] + box[3])/2.0 - 1
    w = xmax-xmin
    h = ymax-ymin
    #x = x*dw   
    #w = w*dw
    #y = y*dh
    #h = h*dh
    return (w,h)
small_object, medium_object, large_object = 0, 0, 0
onlyfiles = [f for f in listdir(imagesPath) if isfile(join(imagesPath, f))]
#onlyxmlfiles = [f for f in listdir(mypath) if join(mypath, f).endswith(".xml")]
#for i in onlyxmlfiles:
for i in onlyfiles:
    #tree = ET.parse("New_Data/Data/dataFormat_7/test/annotations/"+str(i))
    ii = i.split('.')[0]
    tree = ET.parse(annotationsPath+str(ii)+'.xml')
    root = tree.getroot()
    for obj in tree.findall('object'):
        obj_struct = {}
        classs=(obj.find('name').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        b2box=DataFrame(obj_struct).to_numpy()
        xmin=b2box[0][0]
        ymin=b2box[1][0]
        xmax=b2box[2][0]
        ymax=b2box[3][0]
        bboxes = convert(xmin,ymin,xmax,ymax)
        area = bboxes[0]*bboxes[1]
        if classs == 'Light_vehicle':
            obj.find('name').text = "Car"
        '''if classs == 'Dump_truck':
            obj.find('name').text = "Truck"
        if classs == 'Semi-Trailer':
            obj.find('name').text = 'Truck'
        if classs == 'SUV' and area < 1600:
            obj.find('name').text = "Car"
        if classs == 'Sedan' and area < 1600:
            obj.find('name').text = "Car"
            #small_object += 1
            #print('min_area = ', min_area)
        if classs == 'Car':
            #print('max_area = ', max_area)
            root.remove(obj)
        if class:
            medium_object+=1
            #root.remove(obj)'''
        #print('class', obj.find('name').text)
    tree.write("../fisheye_5class/annotations/"+str(ii)+'.xml')
    
    
