# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 20:24:01 2020

@author: Devdarshan
"""
#imports
import argparse
import cv2
import numpy as np

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--image", default='custom/traintest/17.jpg', help="image for prediction")
parser.add_argument("--config", default='custom/cfg/yolov3.cfg', help="YOLO config path")
parser.add_argument("--weights", default='backup/yolov3.weights', help="YOLO weights path")
parser.add_argument("--names", default='custom/classes.names', help="class names path")
args = parser.parse_args()



# Get names of output layers
def getOutputsNames(net):
    layersNames = net.getLayerNames()
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Darw rectanges over detected classes
def draw_pred(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
window_title= "Fire Detector"   
cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)


# Load names of classes
classes = None
with open(args.names, 'r') as f:
    classes = [line.strip() for line in f.readlines()]
print(classes)

#Generate color for each class randomly
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# Define network from configuration file and load the weights
net = cv2.dnn.readNet(args.weights,args.config)

# video capture
cap = cv2.VideoCapture("2.mp4")

while cv2.waitKey(1) < 0:
    
    hasframe, image = cap.read()
    image=cv2.resize(image, (608, 608)) 
    
    blob = cv2.dnn.blobFromImage(image, 1.0/255.0, (608,608), [0,0,0], True, crop=False)
    Width = image.shape[1]
    Height = image.shape[0]
    net.setInput(blob)
    
    outs = net.forward(getOutputsNames(net))
    
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4
    

    
    for out in outs: 
        #print(out.shape)
        for detection in out:
            
        #each detection  has the form like this [center_x center_y width height obj_score class_1_score class_2_score ..]
            scores = detection[5:]#classes scores starts from index 5
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
    
    # apply NMS algorithm on the bounding boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_pred(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
   
    
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
    cv2.putText(image, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
    
    cv2.imshow(window_title, image)
