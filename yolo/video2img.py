import cv2
import numpy as np


cap = cv2.VideoCapture('../newVideos/camera17.avi')
savePath = '../newVideos/camera17_frames/'
i = 0
k = 0


while True:
    success, frame = cap.read()
    name = 'camera17_A_'+str(i)+'.png'
    if k == 200:
        cv2.imwrite(savePath+name,frame)
        i += 1
        k = 0
        print(name)
    k +=1