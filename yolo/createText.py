from importlib.metadata import files
import numpy as np
from os import listdir
from os.path import isfile, join
mypath = '../FishEye_from_dgx/dataFormat_7/train/images/'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
f = open("train.txt","w")
for item in files:
    text = "../FisheyeDataset/images/"+item+"\n"
    f.write(text)
f.close()