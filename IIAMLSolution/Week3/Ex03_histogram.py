#<!--------------------------------------------------------------------------->
from copy import copy
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex03_histogram.py                                        -->
#<!-- Description: Script to represent the pixel distribution function      -->
#<!--            : based on each grayscale level of an input image          -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kopenhagen S.   -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 24/11/2016                                               -->
#<!-- Change     : 24/11/2016 - Development of this exercise                -->
#<!-- Review     : 02/02/2017 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2017020201 $"

########################################################################
import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np

########################################################################
# Construct the argument parser and parse the arguments.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# Create the Matplotlib figures.
fig_imgs = plt.figure("Images")
fig_hist = plt.figure("Histograms")

# This function creates a Matplotlib window and shows four images.
def showImage(image, pos, title="Image", isGray=False):
    sub = fig_imgs.add_subplot(2, 2, pos)
    sub.set_title(title)
    if isGray:
        sub.imshow(image, cmap="gray")
    else:
        sub.imshow(image)
    sub.axis("off")

# This function creates a Matplotlib window and shows four histograms.
def showHistogram(histogram, pos, title="Histogram"):
    sub = fig_hist.add_subplot(2, 2, pos)
    sub.set_title(title)
    plt.xlabel("Bins")
    plt.ylabel("Number of Pixels")
    plt.xlim([0, 256])
    plt.plot(histogram)

# Loads an image from a file passed as argument.
image = cv2.imread(args["image"], cv2.IMREAD_COLOR)
#image = cv2.imread("lena.jpg", cv2.IMREAD_COLOR)

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_gray = cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2RGB)
showImage(image_rgb, 3)
showImage(image_gray, 1)

hist_image_gray = cv2.calcHist([image_gray], [0],None, [256], [0, 255])
showHistogram(hist_image_gray, 1)

shuffled = copy(image_gray)
np.random.shuffle(shuffled)
shuffled = cv2.transpose(shuffled)
np.random.shuffle(shuffled)
showImage(shuffled, 2)

hist_image_shuffled = cv2.calcHist([shuffled], [0],None, [256], [0, 255])
showHistogram(hist_image_shuffled,2)

##

channel_r, channel_g, channel_b = cv2.split(image_rgb)
hist_channel_r = cv2.calcHist([channel_r], [0],None, [256], [0, 255])
hist_channel_g = cv2.calcHist([channel_g], [0],None, [256], [0, 255])
hist_channel_b = cv2.calcHist([channel_b], [0],None, [256], [0, 255])

hist_channel_all = np.zeros([256, 3])
hist_channel_all[:,0] = hist_channel_r.T
hist_channel_all[:,1] = hist_channel_g.T
hist_channel_all[:,2] = hist_channel_b.T

print hist_channel_r.shape

showHistogram(hist_channel_all, 3)

##
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
showImage(image_hsv, 4)

channel_h, channel_s, channel_v = cv2.split(image_hsv)
hist_channel_h = cv2.calcHist([channel_h], [0],None, [256], [0, 255])
hist_channel_s = cv2.calcHist([channel_s], [0],None, [256], [0, 255])
hist_channel_v = cv2.calcHist([channel_v], [0],None, [256], [0, 255])

hist_channel_all2 = np.zeros([256, 3])
hist_channel_all2[:,0] = hist_channel_h.T
hist_channel_all2[:,1] = hist_channel_s.T
hist_channel_all2[:,2] = hist_channel_v.T

showHistogram(hist_channel_all2, 4)

#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->

# Show the Matplotlib windows.
plt.show()
