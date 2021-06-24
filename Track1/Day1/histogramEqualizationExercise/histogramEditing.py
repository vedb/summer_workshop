#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 11:04:35 2020

usage: python histogramEditing.py

@author: michellegreene
"""

# import the necessary libraries
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from skimage import img_as_float
from skimage import exposure
import skimage.io

matplotlib.rcParams['font.size'] = 8

# define plotting function
def plotImageAndHist(image, axes, bins=256):
    
    # load the image, convert to grayscale, and define axes
    image = img_as_float(image)
    axImg, axHist = axes
    axCDF = axHist.twinx()
    
    # display the image
    axImg.imshow(image, cmap=plt.cm.gray)
    axImg.set_axis_off()
    
    # display the histogram
    axHist.hist(image.ravel(), bins=bins, histtype='step', color='black')
    axHist.ticklabel_format(axis='y', style='scientific', scilimits=(0,0))
    axHist.set_xlabel('Pixel Intensity')
    axHist.set_xlim(0,1)
    axHist.set_yticks([])
    
    # display cumulative distribution
    imgCDF, bins = exposure.cumulative_distribution(image, bins)
    axCDF.plot(bins, imgCDF, 'r')
    axCDF.set_yticks([])
    
    return axImg, axHist, axCDF

# load example image
img = skimage.io.imread("chest-xray.jpg", as_gray=True)

# method 1: contrast stretching
p2, p98 = np.percentile(img, (2, 98))
imgRescale = exposure.rescale_intensity(img, in_range=(p2, p98))

# method 2: histogram equalization
imgEq = exposure.equalize_hist(img)

# method 3: adaptive equalization
imgAdapt = exposure.equalize_adapthist(img, clip_limit=0.03)

# display the results
fig = plt.figure(figsize=(8, 5))
axes = np.zeros((2, 4), dtype=np.object)
axes[0, 0] = fig.add_subplot(2, 4, 1)

for i in range(1, 4):
    axes[0, i] = fig.add_subplot(2, 4, 1+i, sharex=axes[0,0], sharey=axes[0,0])
for i in range(0, 4):
    axes[1, i] = fig.add_subplot(2, 4, 5+i)

# plot the original image and histogram
axImg, axHist, axCDF = plotImageAndHist(img, axes[:, 0])
axImg.set_title('Low Contrast Image')
yMin, yMax = axHist.get_ylim()
axHist.set_ylabel('Number of Pixels')
axHist.set_yticks(np.linspace(0, yMax, 5))

axImg, axHist, axCDF = plotImageAndHist(imgRescale, axes[:, 1])
axImg.set_title('Contrast Stretching')

axImg, axHist, axCDF = plotImageAndHist(imgEq, axes[:, 2])
axImg.set_title('Histogram Equalization')

axImg, axHist, axCDF = plotImageAndHist(imgAdapt, axes[:, 3])
axImg.set_title('Adaptive Equalization')

axCDF.set_ylabel('Fraction of total intensity')
axCDF.set_yticks(np.linspace(0, 1, 5))

# prevent overlap of y-axis labels
fig.tight_layout()
plt.show()