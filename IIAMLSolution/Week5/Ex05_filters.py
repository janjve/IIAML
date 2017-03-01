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
    H = np.array([[0, 0, 0],
                  [0, 0, 1],
                  [0, 0, 0]])

    for i in range(n):
        result = cv2.filter2D(result, -1, H, borderType = cv2.BORDER_CONSTANT)

    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->

    return result

#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->



#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->
