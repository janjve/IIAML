#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex03_point_processing.py                                 -->
#<!-- Description: Script to apply a transformation in a pixel of f(x, y)   -->
#<!--            : input image to a pixels in g(x, y) output image          -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kopenhagen S.   -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 01/12/2016                                               -->
#<!-- Change     : 01/12/2016 - Development of this exercise                -->
#<!-- Review     : 08/02/2017 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2017020801 $"

########################################################################
import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np

########################################################################
# Construct the argument parser and parse the arguments.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
#args = vars(ap.parse_args())

# Variables used for point processing.
# a: parameter used for changing contrast.
# b: parameter used for changing brightness.
# c: paramater used for changing negative.
a = 1.
b = 0.
c = 0.

# This method will be performed when the user change the contrast value.
def changeA(value):
    global a
    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->

    a = value / 10.0

    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->
    print "Contrast: ", a, "\t\tBrightness: ", b, "\tNegative: ", c

# This method will be performed when the user change the brightness value.
def changeB(value):
    global b
    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->

    b = value - 128

    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->
    print "Contrast: ", a, "\t\tBrightness: ", b, "\tNegative: ", c

# This method will be performed when the user change the negative value.
def changeC(value):
    global c
    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->

    c = value * 255

    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->
    print "Contrast: ", a, "\t\tBrightness: ", b, "\tNegative: ", c

def contrast(vector, x):
    result = x * vector
    result[result > 255] = 255
    result = result.astype("uint8")
    return result
    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->

def brightness(vector, x):
    result = vector + x
    result[result > 255] = 255
    result[result < 0] = 0
    result = result.astype("uint8")
    return result

    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->

def negative(vector, x):
    result = abs(vector - x)
    result = result.astype("uint8")
    return result 
    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->

def pointProcessing(image, a, b, c):
    result = abs((a * image + b) - c)
    result[result > 255] = 255
    result[result < 0] = 0
    result = result.astype("uint8")
    return result
    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->
    

# Loads a grayscale image from a file passed as argument.
# image = cv2.imread(args["image"], cv2.IMREAD_GRAYSCALE)
image = cv2.imread("lena.jpg", cv2.IMREAD_GRAYSCALE)

# Create a Matplotlib window.
fig = plt.figure()
plt.ion()

# Contrast graphic.
sub1 = fig.add_subplot(2, 2, 1)
sub1.set_title("Contrast")
plt.axis([0, 255, 0, 255])
plt.grid(None, 'major', 'both')

# Brightness graphic.
sub2 = fig.add_subplot(2, 2, 2)
sub2.set_title("Brightness")
plt.axis([0, 255, 0, 255])
plt.grid(None, 'major', 'both')

# Negative graphic.
sub3 = fig.add_subplot(2, 2, 3)
sub3.set_title("Negative")
plt.axis([0, 255, 0, 255])
plt.grid(None, 'major', 'both')

# Point processing graphic.
sub4 = fig.add_subplot(2, 2, 4)
sub4.set_title("Point Processing")
plt.axis([0, 255, 0, 255])
plt.grid(None, 'major', 'both')

# Creates an OpenCV window with three trackbars.
cv2.namedWindow("Point Processing")
cv2.createTrackbar("Contrast",   "Point Processing",  10,  20, changeA)
cv2.createTrackbar("Brightness", "Point Processing", 0, 256, changeB)
cv2.createTrackbar("Negative",   "Point Processing",   0,   1, changeC)

# This vector contains a list of all valid grayscale level.
bins = np.array(range(256))

# Repeat the instructions.
while plt.fignum_exists(fig.number):
    # Call here the transformation function.
    final = pointProcessing(image, a, b, c)

    # Display the resulting image.
    cv2.imshow("Point Processing", final)

    # Clear the plot before showing the new function.
    if (len(sub1.lines)):
        sub1.lines.pop()
    if (len(sub2.lines)):
        sub2.lines.pop()
    if (len(sub3.lines)):
        sub3.lines.pop()
    if (len(sub4.lines)):
        sub4.lines.pop()

    # Contrast changes.
    result = contrast(bins, a)
    sub1 = fig.add_subplot(2, 2, 1)
    plt.plot(bins, result, "r-", linewidth=5)

    # Bightness changes.
    result = brightness(bins, b)
    sub2 = fig.add_subplot(2, 2, 2)
    plt.plot(bins, result, "g-", linewidth=5)

    # Negative changes.
    result = negative(bins, c)
    sub3 = fig.add_subplot(2, 2, 3)
    plt.plot(bins, result, "b-", linewidth=5)

    # Point Processing changes.
    result = pointProcessing(bins, a, b, c)
    sub4 = fig.add_subplot(2, 2, 4)
    plt.plot(bins, result, "k-", linewidth=5)

    # A small pause to render the Matplotlib window.
    plt.pause(0.0001)

# Destroys all of the HighGUI windows.
cv2.destroyAllWindows()
