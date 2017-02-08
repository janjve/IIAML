#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex01_images.py                                           -->
#<!-- Description: Script to read, show, and save images using OpenCV       -->
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
import matplotlib.image as mpimg
import numpy as np

########################################################################
# Construct the argument parser and parse the arguments.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input",  required=True,  help="Path to the input image")
ap.add_argument("-o", "--output", required=False, help="Path to the output image")
args = vars(ap.parse_args())

# Get the input filename
filename = args["input"]

#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->



#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->

# Show the image resolution and the number of channels
channels = image.shape[2] if len(image.shape) == 3 else 1
print "Width: %d pixels." % (image.shape[1])
print "Height: %d pixels." % (image.shape[0])
print "Channels: %d." % (channels)
