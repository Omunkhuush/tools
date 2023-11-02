# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 08:52:16 2021

@author: Erkheme
"""


import os 
import numpy
from pandas import DataFrame
from xml.etree import ElementTree as ET
import cv2 as cv
from os import listdir
from os.path import isfile, join

#mypath = "New_Data/Data/annotationsN/"
mypath = "../fisheye_6class/Data/images/"

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
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
#onlyxmlfiles = [f for f in listdir(mypath) if join(mypath, f).endswith(".xml")]
#for i in onlyxmlfiles:
for i in onlyfiles:
    #tree = ET.parse("New_Data/Data/dataFormat_7/test/annotations/"+str(i))
    ii = i.split('.')[0]
    tree = ET.parse('../fisheye_6class/Data/annotations/'+str(ii)+'.xml')
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
    
    
'''mypath = "New_Data/Data/dataFormat_4/test/annotations/"
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyxmlfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for i in onlyxmlfiles:
    tree = ET.parse("New_Data/Data/dataFormat_4/test/annotations/"+str(i))
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
        if area < 784:
            root.remove(obj)
           # continue
        if classs == 'Scooter' and area < 1600:
            obj.find('name').text = "Moto"
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
            #root.remove(obj)
        #print('class', obj.find('name').text)
    tree.write("New_Data/Data/dataFormat_4/test/annotationsWS/"+str(i))
    

mypath = "New_Data/Data/dataFormat_3/test/annotations/"
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyxmlfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for i in onlyxmlfiles:
    tree = ET.parse("New_Data/Data/dataFormat_3/test/annotations/"+str(i))
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
        if area < 784:
            root.remove(obj)
            #continue
        if classs == 'Scooter' and area < 1600:
            obj.find('name').text = "Moto"
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
            #root.remove(obj)
        #print('class', obj.find('name').text)
    tree.write("New_Data/Data/dataFormat_3/test/annotationsWS/"+str(i))
    
mypath = "New_Data/Data/dataFormat_3/train/annotations/"
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyxmlfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for i in onlyxmlfiles:
    tree = ET.parse("New_Data/Data/dataFormat_3/train/annotations/"+str(i))
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
        if area < 784:
            root.remove(obj)
            #continue
        if classs == 'Scooter' and area < 1600:
            obj.find('name').text = "Moto"
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
            #root.remove(obj)
        #print('class', obj.find('name').text)
    tree.write("New_Data/Data/dataFormat_3/train/annotationsWS/"+str(i))
    
    #tree.write('annotations_MO/'+str(i))
    #tree.write('annotations_LO/'+str(i))
#print('large= ', large_object)
#print('medium= ', medium_object)
print('Pedestrian= ', small_object)
        #images = cv.rectangle(images,(xmin,ymin),(xmax,ymax), color,2)
    #cv.imwrite(i,images)
    #cv.imwrite('./boxes/'+i, images)'''