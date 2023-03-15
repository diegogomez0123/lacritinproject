# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 16:15:29 2022

@author: Diego G
"""

import argparse
import imutils
import cv2
import math
import numpy

square_dict = {}

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

#import image, resize and grayscale. Keep original and resized size ratio to scale back up later
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=1450)
ratio = image.shape[0] / float(resized.shape[0])
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,9)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
contour = imutils.grab_contours(cnts)

count = 0
for c in contour :
    M = cv2.moments(c)
    if(M["m00"]==0): # this is just a line, not 2d shape
        shape = "line" 
    else:
        cpair = [0] * 2
        
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        
        cpair[0] = cX
        cpair[1] = cY
        print(cpair)
        
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True) #above 0.02 and CV detects many non-squares
    
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle" 

        elif len(approx) == 3:
            shape = "triangle"
        elif len(approx) >= 4:
            shape = "somethingelse"
        else:
            shape = "circle"
        
        print(shape)
        if shape == "square":
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                
                square_dict.update({"square" + str(count): cpair})
                count += 1
                
#image output, comment out for rivanna
#cv2.imshow("Image", image)
#cv2.imshow("thresh", thresh)
#cv2.imshow("gray", gray)
#cv2.waitKey(0)
result = len(square_dict)
#print(result)
#print(square_dict)


center_list = list(square_dict.values())
dists = []

#Makes an array of arrays containing distances to each square's center for each square center (X,Y) called dists
dist_index = 0
for i in center_list:
    dists.append([])
    for j in center_list:
        dists[dist_index].append(math.dist(i, j))
    dist_index += 1
            

#cleans dists array by removing values from calculating a square's distance to itself for each sub-array
#removes outlier distances to prevent single residues cross-helix to a main cluster increasing means
count = 0
for i in dists:
    i.remove(0.0)
    mean = numpy.mean(i)
    stdev = numpy.std(i)
    high = (mean + 1.5 *stdev)
    low = (mean - 1.5 * stdev)
    for j in i:
        if j <= low:
            i.remove(j)
        if j >= high:
            i.remove(j)
    del mean
    del stdev
    del high
    del low    
    count += 1       

print(dists)

trimmedmeans = []

#Put means of each sub-array in dists into a single array
count = 0
for i in dists:
    trimmedmeans.append([numpy.mean(i)])
    count += 1

#removes outlier mean distances to prevent cross-helix solo residues from increasing overall mean
#this should not remove the effect of a cross-helix cluster, so means for those helices stay high (excluded)
mean1 = numpy.mean(trimmedmeans)
stdev1 = numpy.std(trimmedmeans)
high1 = (mean1 + 1.1 * stdev1)
low1 = (mean1 - 1.1 * stdev1) 
print(trimmedmeans)
print(stdev1)
print(mean1)

for i, v in enumerate(trimmedmeans):
    if v >= high1:
        trimmedmeans[i] = [0.0]
    if v <= low1:
        trimmedmeans[i] = [0.0]
print(trimmedmeans)

TMF =[]

count = 0
for i in trimmedmeans:
  for j in i:
      TMF.append(j)
      if j == 0.0:
          TMF.remove(j)
  count += 1
        
print(TMF)
FinalMean = numpy.mean(TMF)
print(FinalMean)

#arbitrary cutoff, narrowed down with examples
if FinalMean <= 130:
    print("Check Further") 


    
                
        
    
    