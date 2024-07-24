import numpy as np
import cv2
from os import listdir
from os.path import isfile, join
import os.path

def labelConvert(existLabel,bw,bh):
    boxes = []
    for i in existLabel:
        index, x, y, w, h = map(float, i.split())
        x1 = int((x - w / 2) * bw)
        x2 = int((x + w / 2) * bw)
        y1 = int((y - h / 2) * bh)
        y2 = int((y + h / 2) * bh)
        boxes.append([x1,y1,x2,y2])
    return boxes

def labelUpdate(imageLabelPath,existlabel, savePath):
    imageLabel = open(imageLabelPath,'r')
    imageLabel = imageLabel.readlines()
    imageLabel.extend(existlabel)
    f = open(savePath,'w')
    for i in imageLabel:
        f.write(i)
    f.close()

imagesPath = '/home/munkhuush/Desktop/projects/robocone/dst/all_images/'
labelsPath = '/home/munkhuush/Desktop/projects/robocone/dst/all_labels/'
maskPath =  '/home/munkhuush/Desktop/projects/robocone/export/'

imageSavePath = '/home/munkhuush/Desktop/projects/robocone/newData/images/'
labelSavePath = '/home/munkhuush/Desktop/projects/robocone/newData/labels/'
#images = [f for f in listdir(imagesPath) if isfile(join(imagesPath,f))]
images = [file for file in os.listdir(imagesPath) if file.endswith('.png')]
masks = [file for file in os.listdir(maskPath) if file.endswith('.png')]

# print(len(images))
# print(len(masks))
# print(masks[0])

folderId = ['50-27', '50-37', '17-33']

for g in folderId:
    mask_list = [element for element in masks if g in element]
    image_list = [element for element in images if g in element]
    #print(g, len(mask_list), len(image_list), int(len(image_list)/len(mask_list)))
    
    total = 0
    tot = 0
    for i in range(0,len(mask_list)):
        mask_img = cv2.imread(maskPath + mask_list[i])
        bh,bw,channels = mask_img.shape
        f = open(maskPath+mask_list[i].split(".")[0]+'.txt')
        label = f.readlines()
        converted_label = labelConvert(label,bw,bh)
        pts=[]
        for q in converted_label:
            x_min, y_min, x_max, y_max = q
            pts.extend([(x_min, y_min), (x_min, y_max), (x_max, y_min), (x_max, y_max)])
        pts_array = np.array(pts, dtype=np.int32)
        end = 11
        if g == folderId[2]:
            end = 9
        elif g == folderId[1]:
            end = 12
        for j in range(end):
            tot = total+j
            if tot >= len(image_list):
                break 
            imageName = image_list[tot]
            image = cv2.imread(imagesPath + imageName)
            mask = np.zeros_like(image)
            hull = cv2.convexHull(pts_array)
            cv2.fillPoly(mask, [hull], color=(255, 255, 255))
            out = np.where(mask == np.array([255, 255, 255]), mask_img, image)
            labelPath = labelsPath+imageName.split(".")[0]+'.txt'
            labelUpdate(labelPath, label,labelSavePath+imageName.split(".")[0]+'.txt')
            cv2.imwrite(imageSavePath+imageName, out)
            print(i,j, total+j)
        total = tot+1
    