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
    image_rect = image.copy()
    for _ in xrange(numOfScales):
        image_rect = cv2.pyrDown(image_rect, tuple(np.multiply(image_rect.shape[:2], 0.5)))
    matched = cv2.matchTemplate(image_rect, template, cv2.TM_CCORR_NORMED)

    area = template.shape[:2]
    rows, cols = matched.shape[:2]
    for x in xrange(rows):
        for y in xrange(cols):
            if matched[x,y] >= threshold:
                p1 = (y*(numOfScales+1), x*(numOfScales+1))
                p2 = tuple(np.add(p1, area))
                cv2.rectangle(image, p1, p2, (0,0,255), 2) # Could scale threshold with value

    showImages(CrossCorrelation = matched, Original_image_and_possible_matches = image,Template = template)
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
"""
# ================================ 5.05 (a) ================================= #
image = cv2.imread(filename, cv2.IMREAD_ANYCOLOR)
area = selectArea(image)

template = image[area[0][1]:area[1][1], area[0][0]:area[1][0]]
template = cv2.cvtColor(template, cv2.COLOR_RGB2BGR)
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#showImages(Lena = image, Eye = template)
# ================================ 5.05 (a) ================================= #



# ================================ 5.05 (b) ================================= #
matched1 = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
matched2 = cv2.matchTemplate(image, template, cv2.TM_SQDIFF_NORMED)
matched3 = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

#showImages(Lena = image, Matched1 = matched1, Matched2 = matched2, Matched3 = matched3)
# ================================ 5.05 (b) ================================= #



# ================================ 5.05 (c) ================================= #
min, max, min_p, max_p = cv2.minMaxLoc(matched3)
max_p2 = tuple(max_p + np.subtract(area[1], area[0]))

image_with_match = image.copy()
cv2.rectangle(image_with_match, max_p, max_p2, (0,0,255), 2)
#showImages(Lena = image, Match = image_with_match)
# ================================ 5.05 (c) ================================= #
"""


# ================================ 5.05 (d) ================================= #
p_image = cv2.imread(pattern, cv2.IMREAD_ANYCOLOR)
p_area = selectArea(p_image)

p_template = p_image[p_area[0][1]:p_area[1][1], p_area[0][0]:p_area[1][0]]
p_template = cv2.cvtColor(p_template, cv2.COLOR_RGB2BGR)
p_image = cv2.cvtColor(p_image, cv2.COLOR_RGB2BGR)

# Match
p_matched1 = cv2.matchTemplate(p_image, p_template, cv2.TM_CCORR_NORMED)
p_matched2 = cv2.matchTemplate(p_image, p_template, cv2.TM_SQDIFF_NORMED)
p_matched3 = cv2.matchTemplate(p_image, p_template, cv2.TM_CCOEFF_NORMED)

#showImages(Pattern = p_image, Matched1 = p_matched1, Matched2 = p_matched2, Matched3 = p_matched3)

# Match pyramide
def matchAndPrint(im, template):
    p_matched1 = cv2.matchTemplate(im, template, cv2.TM_CCORR_NORMED)
    p_matched2 = cv2.matchTemplate(im, template, cv2.TM_SQDIFF_NORMED)
    p_matched3 = cv2.matchTemplate(im, template, cv2.TM_CCOEFF_NORMED)
    showImages(Pattern = p_image, Matched1 = p_matched1, Matched2 = p_matched2, Matched3 = p_matched3)

p_image_down2 = cv2.pyrDown(p_image, tuple(np.multiply(p_image.shape[:2], 0.5)))
p_image_down4 = cv2.pyrDown(p_image_down2, tuple(np.multiply(p_image_down2.shape[:2], 0.5)))
p_image_down8 = cv2.pyrDown(p_image_down4, tuple(np.multiply(p_image_down4.shape[:2], 0.5)))


#matchAndPrint(p_image_down2, p_template)
#matchAndPrint(p_image_down4, p_template)
#matchAndPrint(p_image_down8, p_template)

# ================================ 5.05 (d) ================================= #



# ================================ 5.05 (f) ================================= #
matchAll(p_image, p_template, 0.95)
# ================================ 5.05 (f) ================================= #

#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->