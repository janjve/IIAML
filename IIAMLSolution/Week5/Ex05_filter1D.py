#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex05_filter1D.py                                         -->
#<!-- Description: Script to apply a mean filter in an 1D pulse signal      -->
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
ap.add_argument("-n", "--number", required=False, help="The signal size")
args = vars(ap.parse_args())

def onChangeCurrentInterval(value):
    """This function change the current interval to be filtered."""
    global current
    current = value

def onChangeKernel(value):
    """This function defines the kernel size."""
    global kernel

    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->
    
    # ================================ 5.01 (b) ================================= #
    kernel = value + (value+1) % 2
    # ================================ 5.05 (b) ================================= #

    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->

# Define the size of the pulse signal.
n = 50
if args["number"] != None:
    n = int(args["number"])

# Interval from 0 to n (x-axis).
interval = range(n)

#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->

# ================================ 5.01 (a) ================================= #
pulse = np.random.normal(scale=2.0, size=n)
pulse = np.abs(pulse)
# ================================ 5.05 (a) ================================= #

#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->

# Get the maximum value generate in the signal pulse.
max_noise = pulse.max()

# Create one Matplot windows to visualize an 1D function.
fig = plt.figure("1D Filtering")

original_ax = fig.add_subplot(211)
original_ax.set_title("Original Function")
original_ax.set_xlim([-1, n])
original_ax.set_ylim([0, max_noise + 10])

smoothed_ax = fig.add_subplot(212)
smoothed_ax.set_title("Smoothed Function")
smoothed_ax.set_xlim([-1, n])
smoothed_ax.set_ylim([0, max_noise + 10])

# OpenCV window with current interval and kernel trackbars.
cv2.namedWindow("Trackbars", cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar("Current", "Trackbars", 0, n, onChangeCurrentInterval)
cv2.createTrackbar("Kernel", "Trackbars", 2, 10, onChangeKernel)

current = 0
kernel = 5
image = np.zeros((1, 640), np.uint8)
cv2.imshow("Trackbars", image)

# Show the original distribuition.
original_ax.vlines(interval, [0], pulse)
original_ax.plot(interval, pulse, "ko")

# Vector to manager the vertical lines.
lines = []

# Repeat the instructions.
while plt.fignum_exists(fig.number):

    # Clear the plot before showing the new function.
    if (len(smoothed_ax.lines)):
        smoothed_ax.lines.pop()
        lines.remove()

    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->
    
    # ================================ 5.01 (c) ================================= #
    lines = smoothed_ax.vlines(x=interval, ymin=[0], ymax=pulse[:current])

    # ================================ 5.05 (c) ================================= #
    
    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->

    # A small pause to render the Matplotlib window.
    plt.pause(0.0001)

# Destroys all of the HighGUI windows.
cv2.destroyAllWindows()
