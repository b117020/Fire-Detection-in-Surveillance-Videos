# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 04:16:07 2020

@author: Devdarshan
"""
import os
from imutils import paths

path = "Fire/"
path2 = "images/"

imagePaths = list(paths.list_images(path))

import cv2
i=0
for imagePath in imagePaths:
		# load the image and resize it to be a fixed 128x128 pixels,
		# ignoring aspect ratio
    print(imagePath)
    image = cv2.imread(imagePath)
    image = cv2.resize(image, (608, 608))
    cv2.imwrite(os.path.join(path2,"{}.jpg").format(i),image)
    i+=1
