
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join, isdir
import os.path

folder = 'train' 
imagesPath = '../newImages/'+folder+'/images/'
labelPath = '../newImages/'+folder+'/labels/'
savePath = '../newImages/'+folder+'/check/'
#folders = [f for f in listdir(mypath) if isdir(join(mypath, f))]
total = 0
colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0),
          (0, 255, 255), (204, 0, 102)]

classes = ['Bus', 'Bike', 'Car', 'Pedestrian', 'Truck']

notFoundFiles = []
indexRange = []
# for item in folders:

images = [f for f in listdir(imagesPath) if isfile(join(imagesPath, f))]
numberOfObject = 0
for i in images:
    img = cv2.imread(imagesPath+str(i))
    dh, dw, _ = np.shape(img)
    labelName = i.split(".")[0]+'.txt'
    if os.path.isfile(labelPath+labelName) != True:
        notFoundFiles.append(labelPath+labelName)
        print("file not found:", labelPath+labelName)
        continue
    fl = open(labelPath+labelName, 'r')
    data = fl.readlines()
    fl.close()
    for dt in data:
        index, x, y, w, h = map(float, dt.split(' '))
        j = int(index)
        # if j == 4:
        #     j = 2
        # if j == 5:
        #     j = 4
        color = colors[j]
        l = int((x - w / 2) * dw)
        r = int((x + w / 2) * dw)
        t = int((y - h / 2) * dh)
        b = int((y + h / 2) * dh)
        if l < 0:
            l = 0
        if r > dw - 1:
            r = dw - 1
        if t < 0:
            t = 0
        if b > dh - 1:
            b = dh - 1
        cv2.rectangle(img, (l, t), (r, b), color, 1)
        numberOfObject += 1
    cv2.imwrite(savePath+str(i), img)
    print(savePath+str(i))
print("not found Files:")
for i in notFoundFiles:
    print(i)
print(indexRange)
print(numberOfObject)
