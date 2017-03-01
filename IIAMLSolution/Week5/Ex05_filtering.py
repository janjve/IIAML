#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex05_filtering.py                                        -->
#<!-- Description: Script to generate and remove noise using filters        -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kopenhagen S.   -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 15/12/2017                                               -->
#<!-- Change     : 15/12/2017 - Development of this exercise                -->
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
ap.add_argument("-i", "--image", required=True, help="Path to the image")
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

def changeRow(value):
    """This function change the number of the selected row."""
    global row
    row = value
    updateImage()

def updateImage():
    """Update the input image to show the selected region."""
    # Draw a white line in the processed image row.
    processed = cv2.line(image.copy(), (0, row), (w, row), 255)
    cv2.imshow("image", processed)

def to_uint8(data):
    """This function convert the vector data to unsigned integer 8-bits."""
    # maximum pixel
    latch = np.zeros_like( data )
    latch[:] = 255

    # minimum pixel
    zeros = np.zeros_like( data )

    # unrolled to illustrate steps
    d = np.maximum( zeros, data )
    d = np.minimum( latch, d )

    # cast to uint8
    return np.asarray( d, dtype="uint8" )



#<!--------------------------------------------------------------------------->
#<!--                  GENERATE RANDOM NOISE DISTRIBUTION                   -->
#<!--------------------------------------------------------------------------->

def saltAndPepperNoise(image, density):
    noised = image.copy()
    h, w = noised.shape

    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->

    # ============================== 5.01 (a) [i] =============================== #
    
    # ============================== 5.01 (a) [i] =============================== #

    return noised

def gaussianNoise(image, mu, sigma):
    noised = image.copy()
    h, w = noised.shape

    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->

    # ============================== 5.01 (a) [ii] ============================== #
    
    # ============================== 5.01 (a) [ii] ============================== #

    return noised

def uniformNoise(image, low, high):
    noised = image.copy()
    h, w = noised.shape

    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->

    # ============================= 5.01 (a) [iii] ============================== #
    
    # ============================= 5.01 (a) [iii] ============================== #

    return noised



#<!--------------------------------------------------------------------------->
#<!--                                FILTERS                                -->
#<!--------------------------------------------------------------------------->

def saltAndPepperFilter(image, n=3):
    filtered = image.copy()
    h, w = filtered.shape
    
    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->

    # ============================= 5.01 (c)(e)(f) ============================== #
    
    # ============================= 5.01 (c)(e)(f) ============================== #

    return filtered

def gaussianFilter(image, n=5):
    filtered = image.copy()
    h, w = filtered.shape
    
    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->
    
    # =============================== 5.01 (c)(e) =============================== #
    
    # =============================== 5.01 (c)(e) =============================== #

    return filtered

def uniformFilter(image, n=5):
    filtered = image.copy()
    h, w = filtered.shape
    
    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->
    
    # =============================== 5.01 (c)(e) =============================== #
    
    # =============================== 5.01 (c)(e) =============================== #

    return filtered



#<!--------------------------------------------------------------------------->
#<!--                              INPUT IMAGE                              -->
#<!--------------------------------------------------------------------------->

# Loads an image from a file passed as argument.
image = cv2.imread(args["image"], cv2.IMREAD_GRAYSCALE)



#<!--------------------------------------------------------------------------->
#<!--                      ADD NOISE TO THE INPUT IMAGE                     -->
#<!--------------------------------------------------------------------------->

#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->

# ================================ 5.01 (b) ================================= #
# Create an image with salt and pepper noise.
saltAndPepper = saltAndPepperNoise(image, 0)

# Create an image with Gaussian noise.
gaussian = gaussianNoise(image, 0, 0)

# Create an image with uniform noise.
uniform = uniformNoise(image, 0, 0)

# Show the original image and the noised images.
showImages(Uniform=uniform, Gaussian=gaussian, Salt_and_Pepper=saltAndPepper,
           Original=image)
# ================================ 5.01 (b) ================================= #

#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->



#<!--------------------------------------------------------------------------->
#<!--                      ADD NOISE TO THE INPUT IMAGE                     -->
#<!--------------------------------------------------------------------------->

# Filter the salt and pepper noise.
saltAndPepperFiltered = saltAndPepperFilter(saltAndPepper)

# Filter the Gaussian noise.
gaussianFiltered = gaussianFilter(gaussian)

# Filter the uniform noise.
uniformFiltered = uniformFilter(uniform)

# Show the original image and the noised images.
showImages(Uniform=uniformFiltered, Gaussian=gaussianFiltered,
           Salt_and_Pepper=saltAndPepperFiltered, Original=image)



#<!--------------------------------------------------------------------------->
#<!--                  SHOW NOISE AS A 1D IMPULSE FUNCTION                  -->
#<!--------------------------------------------------------------------------->

# Image resolution
h, w = image.shape

# Create a Matplotlib window.
fig1 = plt.figure("Distributions")

# Image graphic.
sub1 = fig1.add_subplot(2, 2, 1)
sub1.set_title("Original")
sub1.axis([0, w, 0, 255])
sub1.grid(None, 'major', 'both')

# Salt and Pepper graphic.
sub2 = fig1.add_subplot(2, 2, 2)
sub2.set_title("Salt and Pepper")
sub2.axis([0, w, 0, 255])
sub2.grid(None, 'major', 'both')

# Gaussian graphic.
sub3 = fig1.add_subplot(2, 2, 3)
sub3.set_title("Gaussian")
sub3.axis([0, w, 0, 255])
sub3.grid(None, 'major', 'both')

# Uniform graphic.
sub4 = fig1.add_subplot(2, 2, 4)
sub4.set_title("Uniform")
sub4.axis([0, w, 0, 255])
sub4.grid(None, 'major', 'both')

# Create a Matplotlib window.
fig2 = plt.figure("Filtered Distributions")

# Image graphic.
sub5 = fig2.add_subplot(2, 2, 1)
sub5.set_title("Original")
sub5.axis([0, w, 0, 255])
sub5.grid(None, 'major', 'both')

# Salt and Pepper graphic.
sub6 = fig2.add_subplot(2, 2, 2)
sub6.set_title("Salt and Pepper")
sub6.axis([0, w, 0, 255])
sub6.grid(None, 'major', 'both')

# Gaussian graphic.
sub7 = fig2.add_subplot(2, 2, 3)
sub7.set_title("Gaussian")
sub7.axis([0, w, 0, 255])
sub7.grid(None, 'major', 'both')

# Uniform graphic.
sub8 = fig2.add_subplot(2, 2, 4)
sub8.set_title("Uniform")
sub8.axis([0, w, 0, 255])
sub8.grid(None, 'major', 'both')

# Current row.
row = 0

# Create an OpenCV window.
cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar("row", "image", 0, h - 1, changeRow)
updateImage()

# This vector contains a list of all valid grayscale level.
bins = np.array(range(w))

# Repeat the instructions.
while (plt.fignum_exists(fig1.number) and
       plt.fignum_exists(fig2.number)):

    # Clear the plot before showing the new function.
    if (len(sub1.lines)):
        sub1.lines.pop()
    if (len(sub2.lines)):
        sub2.lines.pop()
    if (len(sub3.lines)):
        sub3.lines.pop()
    if (len(sub4.lines)):
        sub4.lines.pop()
    if (len(sub5.lines)):
        sub5.lines.pop()
    if (len(sub6.lines)):
        sub6.lines.pop()
    if (len(sub7.lines)):
        sub7.lines.pop()
    if (len(sub8.lines)):
        sub8.lines.pop()

    # Image distribuition.
    result = image[row, :]
    sub1 = fig1.add_subplot(2, 2, 1)
    sub1.plot(bins, result, "r-", linewidth=1)

    # Salt and pepper distribuition.
    result = saltAndPepper[row, :]
    sub2 = fig1.add_subplot(2, 2, 2)
    sub2.plot(bins, result, "g-", linewidth=1)

    # Gaussian distribuition.
    result = gaussian[row, :]
    sub3 = fig1.add_subplot(2, 2, 3)
    sub3.plot(bins, result, "b-", linewidth=1)

    # Gaussian distribuition.
    result = uniform[row, :]
    sub4 = fig1.add_subplot(2, 2, 4)
    sub4.plot(bins, result, "k-", linewidth=1)

    # Image filtered distribuition.
    result = image[row, :]
    sub5 = fig2.add_subplot(2, 2, 1)
    sub5.plot(bins, result, "r-", linewidth=1)

    # Salt and pepper filtered distribuition.
    result = saltAndPepperFiltered[row, :]
    sub6 = fig2.add_subplot(2, 2, 2)
    sub6.plot(bins, result, "g-", linewidth=1)

    # Gaussian filtered distribuition.
    result = gaussianFiltered[row, :]
    sub7 = fig2.add_subplot(2, 2, 3)
    sub7.plot(bins, result, "b-", linewidth=1)

    # Gaussian filtered distribuition.
    result = uniformFiltered[row, :]
    sub8 = fig2.add_subplot(2, 2, 4)
    sub8.plot(bins, result, "k-", linewidth=1)

    # A small pause to render the Matplotlib window.
    plt.pause(0.0001)

# Destroys all of the HighGUI windows.
cv2.destroyAllWindows()
