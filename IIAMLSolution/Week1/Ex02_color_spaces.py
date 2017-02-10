#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex02_color_spaces.py                                     -->
#<!-- Description: Script to convert the loaded images into two different   -->
#<!--            : color spaces (RGB and HSV)                               -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kopenhagen S.   -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 25/11/2016                                               -->
#<!-- Change     : 25/11/2016 - Development of this exercise                -->
#<!-- Review     : 02/02/2017 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2017020201 $"

########################################################################
import numpy as np
import argparse
import cv2

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

########################################################################
# Construct the argument parser and parse the arguments.
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="Path to the image")
#args = vars(ap.parse_args())

# Create the Matplotlib window.
fig = plt.figure()

# Get the input filename
#filename = args["image"]
filename = "Assets/lena.jpg"

#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->
'''
image_bgr = cv2.imread(filename)
image_rgb  = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)

#channel_r, channel_g, channel_b = cv2.split(image_rgb)
channel_h, channel_s, channel_v = cv2.split(image_hsv)
#cv2.imshow("name", channel_v)
#cv2.waitKey()
#cv2.destroyAllWindows()
'''

# orig + gray
'''
sub = fig.add_subplot(1,2,1)
sub.set_title("Original image")
plt.axis("off")
plt.imshow(image_rgb)

sub = fig.add_subplot(1,2,2)
sub.set_title("Grayscale image")
plt.axis("off")
plt.imshow(cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY), cmap='Greys_r')
'''

# f
image = mpimg.imread(filename)
channel_r, channel_g, channel_b = cv2.split(image)
single = np.zeros([image.shape[0], image.shape[1]], dtype=np.uint8)

image_r = cv2.merge([channel_r, single, single])
image_g = cv2.merge([single, channel_g, single])
image_b = cv2.merge([single, single, channel_b])

# Printout
def show(title, im, loc):
    sub = fig.add_subplot(1,3,loc)
    sub.set_title(title)
    plt.axis("off")
    plt.imshow(im)

show("Channel R", image_r, 1)
show("Channel G", image_g, 2)
show("Channel B", image_b, 3)

#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->

# Show the final image.
plt.show()
