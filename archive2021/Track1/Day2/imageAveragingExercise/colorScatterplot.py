#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:18:43 2020

Usage: python colorScatterplot.py

@author: michellegreene
"""

# import the necessary libraries
import numpy as np
import cv2
import glob
from matplotlib import pyplot as plt
import warnings

# suppress silly warnings
warnings.filterwarnings("ignore")

# create lists of desert, forest, and ocean directories
desertList = glob.glob('./Data/Images/desert' + '/' + '*.jpg')
forestList = glob.glob('./Data/Images/forest' + '/' + '*.jpg')
oceanList = glob.glob('./Data/Images/ocean' + '/' + '*.jpg')

# Get image dimensions
N = len(desertList)
testIm = cv2.imread(desertList[0])
h, w = testIm.shape[:-1]

# Initialize image averages
averageDesert = np.zeros((h, w, 3), np.float)
averageForest = np.zeros((h, w, 3), np.float)
averageOcean = np.zeros((h, w, 3), np.float)

# initialize figure
fig = plt.figure()
plt.ion()
fig.canvas.draw()

# create show all images and their running average
for i in range(len(desertList)):
    fig.canvas.draw()
    # read in image examples and compute running averages
    desertExample = cv2.imread(desertList[i])
    desertExample = cv2.cvtColor(desertExample, cv2.COLOR_BGR2RGB)
    averageDesert = (averageDesert*i + desertExample) / (i+1)
    
    forestExample = cv2.imread(forestList[i])
    forestExample = cv2.cvtColor(forestExample, cv2.COLOR_BGR2RGB)
    averageForest = (averageForest*i + forestExample) / (i+1)
    
    oceanExample = cv2.imread(oceanList[i])
    oceanExample = cv2.cvtColor(oceanExample, cv2.COLOR_BGR2RGB)
    averageOcean = (averageOcean*i + oceanExample) / (i+1)
    
    # format the averages
    desertTempAverage = np.array(np.round(averageDesert), dtype=np.uint8)
    forestTempAverage = np.array(np.round(averageForest), dtype=np.uint8)
    oceanTempAverage = np.array(np.round(averageOcean), dtype=np.uint8)

    # plot the examples and running average
    plt.subplot(231)
    plt.imshow(desertExample)
    plt.axis('off')
    plt.subplot(232)
    plt.imshow(forestExample)
    plt.axis('off')
    plt.subplot(233)
    plt.imshow(oceanExample)
    plt.axis('off')
    plt.subplot(234)
    plt.imshow(desertTempAverage)
    plt.axis('off')
    plt.subplot(235)
    plt.imshow(forestTempAverage)
    plt.axis('off')
    plt.subplot(236)
    plt.imshow(oceanTempAverage)
    plt.axis('off')
    plt.draw()
    plt.pause(.01)
    
# part 2: 3D scatterplot
#input("Press Enter to plot the average pixels...")
# plt.close(fig)
# plt.ioff()
# fig = plt.figure()
# ax = plt.axes(projection='3d')


# # plot the averaged pixels
# red = averageDesert[:,:,0].ravel()
# green = averageDesert[:,:,1].ravel()
# blue = averageDesert[:,:,2].ravel()
# desertFig = ax.scatter(red, green, blue, c="#D95F02", label="Desert")
# red = averageForest[:,:,0].ravel()
# green = averageForest[:,:,1].ravel()
# blue = averageForest[:,:,2].ravel()
# forestFig = ax.scatter(red, green, blue, c="green", label="Forest")
# red = averageOcean[:,:,0].ravel()
# green = averageOcean[:,:,1].ravel()
# blue = averageOcean[:,:,2].ravel()
# oceanFig = ax.scatter(red, green, blue, c="blue", label="Ocean")
# ax.set_xlabel("Red Channel")
# ax.set_ylabel("Green Channel")
# ax.set_zlabel("Blue Channel")
# plt.legend(handles=[desertFig, forestFig, oceanFig])
# plt.show()
