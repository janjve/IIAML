#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex05_template.py                                         -->
#<!-- Description: Script to find small parts in the input image which      -->
#<!--            : match a template image                                   -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kopenhagen S.   -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 27/02/2015                                               -->
#<!-- Change     : 27/02/2015 - Development of this exercise                -->
#<!-- Review     : 22/02/2017 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2017022201 $"

########################################################################
import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np

########################################################################
# Construct the argument parser and parse the arguments.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-p", "--pattern", required=True, help="Path to the pattern")
args = vars(ap.parse_args())

# Selected points on image.
left_point = None
right_point = None
selected = np.zeros((1, 1, 1), np.uint8)

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
        plt.subplot(1, len(images), pos+1)
        plt.title(name)
        plt.imshow(image)

    # Show the images.
    plt.show()

def updateImage():
    """Update the input image to show the selected region."""
    if (left_point is None) | (right_point is None):
        cv2.imshow("Select an area", selected)
        return

    # Draw a rectangle in the selected area.
    processed = selected.copy()
    cv2.rectangle(processed, left_point, right_point, (0, 0, 255), 2)
    cv2.imshow("Select an area", processed)

def onMouse(event, x, y, flags, param):
    """Get the mouse events over an OpenCV windows."""
    global left_point
    global right_point
    
    if  flags & cv2.EVENT_FLAG_LBUTTON:
        left_point = x, y

    if  flags & cv2.EVENT_FLAG_RBUTTON: 
        right_point = x, y

    updateImage()

def selectArea(image):
    """
    This function returns the corners of the selected area as:
    [(UpLeftCorner), (DownRightCorner)]

    Use the right and left buttons of mouse and click on the image to set the
    region of interest.

    When you finish, you have to press the following key in your keyboard:
    Enter - OK
    ESC   - Exit (Cancel)
    """
    global selected
    global left_point
    global right_point

    left_point  = None
    right_point = None

    # Create an OpenCV window.
    cv2.namedWindow("Select an area", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("Select an area", onMouse)

    # Show the input image.
    selected = image.copy()
    updateImage()

    # Handle with the mouse events.
    while True:
        # Get one keyboard event.
        ch = cv2.waitKey()

        # Cancel if the user press ESC.
        if ch == 27:
            return

        # Stop the while when press ENTER.
        if ch == 13:
            cv2.destroyWindow("Select an area")
            break

    # Create the selected points structure.
    points = []

    up_left    = (min(left_point[0], right_point[0]),
                  min(left_point[1], right_point[1]))
    down_right = (max(left_point[0], right_point[0]),
                  max(left_point[1], right_point[1]))

    points.append(up_left)
    points.append(down_right)
 
    # Return the final result.
    return points

def matchAll(image, template, threshold, numOfScales=0):
    """
    This function does the cross correlation in an input image (image) and a
    template (template) and shows a rectangle around each possible match in the
    original image (i.e. larger than threshold).
    """
    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->

    # ================================ 5.05 (e) ================================= #
    
    # ================================ 5.05 (e) ================================= #

    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->

# Create the Matplotlib window.
# There is a bug on macOS that it is not possible to open an OpenCV windows
# before openning a Matplotlib windows.
fig = plt.figure()
plt.close()

# Get the input filename.
filename = args["image"]
pattern  = args["pattern"]

#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->

# ================================ 5.05 (a) ================================= #

# ================================ 5.05 (a) ================================= #



# ================================ 5.05 (b) ================================= #

# ================================ 5.05 (b) ================================= #



# ================================ 5.05 (c) ================================= #

# ================================ 5.05 (c) ================================= #



# ================================ 5.05 (d) ================================= #

# ================================ 5.05 (d) ================================= #



# ================================ 5.05 (e) ================================= #

# ================================ 5.05 (e) ================================= #

#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->