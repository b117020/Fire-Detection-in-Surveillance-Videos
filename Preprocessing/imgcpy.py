# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 00:42:13 2020

@author: Devdarshan
"""

import os,shutil

path = "yolo/"
files= os.listdir(path)
ls = []
for item in files:
    i = item.replace(".txt", "")
    ls.append(i)
    
path1 = "image2/"
path2 = "set2/" 
files = os.listdir(path1)
for item in files:
    i = item.replace(".jpg","")
    print(item)
    if i in ls:
        shutil.copy(os.path.join(path1,item), path2 )
        


