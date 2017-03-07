#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex05_filters.py                                          -->
#<!-- Description: Script to create and use sharpen and shift filters       -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kopenhagen S.   -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 23/02/2017                                               -->
#<!-- Change     : 23/02/2017 - Development of this exercise                -->
#<!-- Review     : 23/02/2017 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2017022301 $"

########################################################################
import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np

########################################################################
# Construct the argument parser and parse the arguments.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Input Image")
args = vars(ap.parse_args())

def showImages(**images):
    """Show multiple images using matplotlib."""
    # When a double-starred parameter is declared such as $**images$, then all
    # the keyword arguments from that point till the end are collected as a
    # dictionary called $'images'$.

    # Create a new matplotlib window.
    plt.figure()

    # Set the default colormap to gray and apply to current image if any.
    plt.gray()

    # Enumarate the ID, window name and images passed as parameter.
    for (pos, (name, image)) in enumerate(images.items()):
        # Show the image in a new subplot.
        plt.subplot(2, len(images) / 2, pos+1)
        plt.title(name)
        plt.imshow(image)

    # Show the images.
    plt.show()

def shiftToLeft(image, n):
    """Shift all pixel of the input image n column to the left."""
    result = image.copy()
    
    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->

    # Change this Python code.
    H = np.zeros((1, (n*2+1)))
    H[0,n*2] = 1

    #for i in range(n):
    result = cv2.filter2D(result, -1, H, borderType = cv2.BORDER_CONSTANT)

    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->

    return result

def shiftToRight(image, n):
    """Shift all pixel of the input image n column to the right."""
    result = image.copy()
    H = np.zeros((1, (n*2+1)))
    H[0,0] = 1
    result = cv2.filter2D(result, -1, H, borderType = cv2.BORDER_CONSTANT)
    return result

def shiftToUp(image, n):
    """Shift all pixel of the input image n column to the up."""
    result = image.copy()
    H = np.zeros(((n*2+1), 1))
    H[n*2,0] = 1
    result = cv2.filter2D(result, -1, H, borderType = cv2.BORDER_CONSTANT)
    return result

def shiftToDown(image, n):
    """Shift all pixel of the input image n column to the down."""
    result = image.copy()
    H = np.zeros(((n*2+1), 1))
    H[0,0] = 1
    result = cv2.filter2D(result, -1, H, borderType = cv2.BORDER_CONSTANT)
    return result

def shiftToDownRight(image, n, m):
    """Shift all pixel of the input image n column to the down right."""
    result = image.copy()
    H = np.zeros((m*2+1, n*2+1))
    H[0,0] = 1

    result = cv2.filter2D(result, -1, H, borderType = cv2.BORDER_CONSTANT)
    return result

#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->
# a)
image = cv2.imread(args['image'], cv2.IMREAD_GRAYSCALE)
base = np.full((3,3), -1, dtype=np.float64)
filter1 = base.copy()
filter1[1,1] = 17
filter1 = filter1 * (1. / np.sum(filter1))

filter2 = base.copy()
filter2[1,1] = 9
filter2 = filter2 * (1. / np.sum(filter2))

filter3 = base.copy()
filter3[1,1] = 100
filter3 = filter3 * (1. / np.sum(filter3))

image_with_filter1 = cv2.filter2D(image, -1, filter1)
image_with_filter2 = cv2.filter2D(image, -1, filter2)
image_with_filter3 = cv2.filter2D(image, -1, filter3)

#print filter1
#print filter2
#print filter3
#showImages(grayscale = image, filter1 = image_with_filter1, filter2 = image_with_filter2, filter3 = image_with_filter3)

# d)
image_with_shiftL = shiftToLeft(image, 20)
image_with_shiftR = shiftToRight(image, 20)
image_with_shiftU = shiftToUp(image, 20)
image_with_shiftD = shiftToDown(image, 20)
image_with_shiftDR = shiftToDownRight(image, 20, 20)
#showImages(shiftL = image_with_shiftL, shiftR = image_with_shiftR, shiftU = image_with_shiftU, shiftD = image_with_shiftD)
showImages(grayscale = image, shiftDR = image_with_shiftDR)


#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->
