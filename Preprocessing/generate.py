# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 03:03:18 2020

@author: Devdarshan
"""

import glob, os


dataset_path = 'D:/COEAI/keras-fire-detection/keras-fire-detection/Robbery_Accident_Fire_Database2/yolofiredetection/darknet/custom/set2'

# Percentage of images to be used for the test set
percentage_test = 10;

# Create and/or truncate train.txt and test.txt
file_train = open('train1.txt', 'w')  
file_test = open('test1.txt', 'w')

# Populate train.txt and test.txt
counter = 1  
index_test = round(100 / percentage_test)  
for pathAndFilename in glob.iglob(os.path.join(dataset_path, "*.jpg")):  
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    if counter == index_test+1:
        counter = 1
        file_test.write(dataset_path + "/" + title + '.jpg' + "\n")
    else:
        file_train.write(dataset_path + "/" + title + '.jpg' + "\n")
        counter = counter + 1
        
file_test.close()
file_train.close()