#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex05_filter2D.py                                         -->
#<!-- Description: Script to apply a mean filter in a grayscale image       -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kopenhagen S.   -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 21/02/2017                                               -->
#<!-- Change     : 21/02/2017 - Development of this exercise                -->
#<!-- Review     : 22/02/2017 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2017022201 $"

########################################################################
import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

########################################################################
# Construct the argument parser and parse the arguments.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->

# ================================ 5.01 (a) ================================= #
image = cv2.imread(args["image"], cv2.IMREAD_GRAYSCALE)
shape = image.shape[:2]
print shape
# ================================ 5.01 (a) ================================= #



# ================================ 5.01 (b) ================================= #
coordinate_matrix = np.meshgrid(range(0,shape[0]), range(0,shape[1]))
# ================================ 5.01 (b) ================================= #

print coordinate_matrix

# ================================ 5.01 (c) ================================= #
fig = plt.figure("3D figure")
ax = fig.gca (projection ="3d")
ax.plot_surface(coordinate_matrix[0], coordinate_matrix[1], image, cmap=cm.gray)
# ================================ 5.01 (c) ================================= #



# ================================ 5.01 (d) ================================= #
image_blur = cv2.GaussianBlur(image, (5,5), 10)
# ================================ 5.01 (d) ================================= #



# ================================ 5.01 (e) ================================= #
fig = plt.figure("3D figure blur")
ax = fig.gca (projection ="3d")
ax.plot_surface(coordinate_matrix[0], coordinate_matrix[1], image_blur, cmap=cm.gray)
# ================================ 5.01 (e) ================================= #

#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->
plt.show()