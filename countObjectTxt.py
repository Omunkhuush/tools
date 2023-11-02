from cProfile import label
from os.path import isfile, join, isdir
from os import listdir
folder = 'train'
labelPath = '../AllLabeled_9_class/'+folder+'/labels_9class/'
files = [f for f in listdir(labelPath) if isfile(join(labelPath, f))]
totalObjects = 0
totalClasses = []
classes = ['Bike', 'Pedestrian', 'Car', 'SUV', 'Taxi', 'Sedan', 'Truck', 'Bus', 'Van']
for i in files:
    fl = open(labelPath+i, 'r')
    data = fl.readlines()
    fl.close()
    for dt in data:
        index, x, y, w, h = map(float, dt.split(' '))
        totalObjects +=1
        if classes[int(index)] in totalClasses:
            continue
        else:
           totalClasses.append(classes[int(index)]) 
print(totalObjects)
print(totalClasses)
print(len(totalClasses))