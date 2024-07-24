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
        boxes.append([index,x1,y1,x2,y2])
    return boxes

def labelUpdate(imageLabelPath,existlabel, savePath):
    imageLabel = open(imageLabelPath,'r')
    imageLabel = imageLabel.readlines()
    imageLabel.extend(existlabel)
    f = open(savePath,'w')
    for i in imageLabel:
        f.write(i)
    f.close()

def replace(background, object,new_bbox):
    x1,y1, x2, y2 = new_bbox
    roi = background[y1:y1+(y2-y1), x1:x1+(x2-x1)]
    if roi.shape[:2] != object.shape[:2]:
        object = cv2.resize(object, (roi.shape[1], roi.shape[0]))
    
    object2gray = cv2.cvtColor(object,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(object2gray, 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    background_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
    object_fg = cv2.bitwise_and(object,object,mask = mask)
    dst = cv2.add(background_bg,object_fg)
    background[y1:y1+(y2-y1), x1:x1+(x2-x1)] = dst
    return background

def is_overlapping(existing_boxes, new_box):
    #new_box = [new_box[0],new_box[1],new_box[2]-new_box[0],new_box[3]-new_box[1]]
    for box in existing_boxes:
        if (box[1] < new_box[2] and new_box[0] < box[3] and
            box[2] < new_box[3] and new_box[1] < box[4]):
            #print(box,new_bbox)
            return True
    return False

imagesPath = '/home/munkhuush/Desktop/projects/robocone/dst/all_images/'
labelsPath = '/home/munkhuush/Desktop/projects/robocone/dst/all_labels/'
maskPath =  '/home/munkhuush/Desktop/projects/robocone/export/'

imageSavePath = '/home/munkhuush/Desktop/projects/robocone/resized_data/images/'
labelSavePath = '/home/munkhuush/Desktop/projects/robocone/resized_data/labels/'

images = [file for file in os.listdir(imagesPath) if file.endswith('.png')]
masks = [file for file in os.listdir(maskPath) if file.endswith('.png')]

folderId = ['50-27', '50-37', '17-33']


for g in folderId:
    mask_list = [element for element in masks if g in element]
    image_list = [element for element in images if g in element]

    total = 0
    tot = 0

    for i in range(0,len(mask_list)):

        mask_img = cv2.imread(maskPath+mask_list[i])
        bh,bw,channels = mask_img.shape
        f = open(maskPath+mask_list[i].split(".")[0]+'.txt')
        label = f.readlines()
        converted_label = labelConvert(label,bw,bh)

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
            ih, iw,_ = image.shape
            txtName = imageName.split(".")[0]+".txt"
            txt_new_name = imageName.split(".")[0]+"_resized.txt" 
            for cord in converted_label:
                obj = mask_img[cord[2]:cord[4], cord[1]:cord[3]]
                out = replace(image, obj, cord[1:])
                # update label
            labelUpdate(labelsPath+txtName,label,labelSavePath+txt_new_name)

            for cord in converted_label:
                obj = mask_img[cord[2]:cord[4], cord[1]:cord[3]]
                x1 = cord[1]-int((cord[3]-cord[1])/2)
                y1 = cord[2]-int(cord[4]-cord[2])
                if x1 < 0 or y1 < 0:
                    continue
                h,w,_ = obj.shape
                points = (int(w*0.8),int(h*0.8))
                obj = cv2.resize(obj,points,interpolation= cv2.INTER_LINEAR)
                new_cord = [x1,y1,x1+obj.shape[1],y1+obj.shape[0]]

                ff = open(labelSavePath+txt_new_name)
                img_label = ff.readlines()
                img_c_label = labelConvert(img_label,iw,ih)
                overlap = is_overlapping(img_c_label,new_cord)
                if not overlap:
                    out = replace(out, obj, new_cord)
                    xmin = new_cord[0]
                    ymin = new_cord[1]
                    xmax = new_cord[2]
                    ymax = new_cord[3]
                    x = ((xmin+xmax)/2)/iw
                    y = ((ymin+ymax)/2)/ih
                    wh = (xmax-xmin)/iw
                    he = (ymax-ymin)/ih
                    uplabel = str(cord[0]) + " "+str(x)+" "+str(y)+" "+str(wh)+" "+str(he)+'\n'
                    labelUpdate(labelSavePath+txt_new_name,uplabel,labelSavePath+txt_new_name)
                    imgName_resized = imageName.split(".")[0]+"_resized.png"
                    cv2.imwrite(imageSavePath+imgName_resized, out)

            print(i,j, total+j)
        total = tot+1



# pts=[]
# for q in converted_label:
#     x_min, y_min, x_max, y_max = q
#     pts.extend([(x_min, y_min), (x_min, y_max), (x_max, y_min), (x_max, y_max)])
# pts_array = np.array(pts, dtype=np.int32)
# end = 11
# if g == folderId[2]:
#     end = 9
# elif g == folderId[1]:
#     end = 12
# for j in range(end):
#     tot = total+j
#     if tot >= len(image_list):
#         break 
#     imageName = image_list[tot]
#     image = cv2.imread(imagesPath + imageName)
#     mask = np.zeros_like(image)
#     hull = cv2.convexHull(pts_array)
#     cv2.fillPoly(mask, [hull], color=(255, 255, 255))
#     out = np.where(mask == np.array([255, 255, 255]), mask_img, image)
#     labelPath = labelsPath+imageName.split(".")[0]+'.txt'
#     labelUpdate(labelPath, label,labelSavePath+imageName.split(".")[0]+'.txt')
#     cv2.imwrite(imageSavePath+imageName, out)
#     print(i,j, total+j)
# total = tot+1
