#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : fundamentalMatrix.py                                     -->
#<!-- Description: Script to calculate the Fundamental Matrix (F) based on  -->
#<!--            : epipolar geometry                                        -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kobenhavn S.    -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: You DO NOT need to change this file                      -->
#<!-- Date       : 25/04/2017                                               -->
#<!-- Change     : 25/04/2017 - Creation of this script                     -->
#<!-- Review     : 25/04/2017 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2017042501 $"

########################################################################
import cv2
import numpy as np
from matplotlib import pyplot as plt
from collections import deque

from CaptureVideo.CaptureVideo import CaptureVideo

########################################################################
def eyeMouseEvent(event, x, y, flag, param):
    """This is an example of a calibration process using the mouse clicks."""
    # Check if the system is frozen.
    if not isFrozen:
        return

    # Insert a new point in the calibration process.
    if event == cv2.EVENT_LBUTTONDOWN:
        addNewPoint((x, y, 1))

def addNewPoint(point):
    """Insert a new point in the queue."""
    # Global variables.
    global queue
    global stereo

    # Get the current queue size.
    size = len(queue)

    # Check if the queue is full.
    if size == queue.maxlen:
        return

    # Defines the color used for draw the circle and the line.
    color = (0, 0, 255) if size % 2 == 0 else (255, 0, 0)

    # Draw a circle in the selected point.
    cv2.circle(stereo, point[:2], 3, color, thickness=-1)

    # Adjust the right click to correct position.
    if size % 2 != 0:
        point = (point[0] - stereo.shape[1] / 2, point[1], 1)

    # Insert the new point in the queue.
    queue.append(point)

    # Check if the queue is full now.
    if size + 1 == queue.maxlen:
        fundamentalMatrix()

def fundamentalMatrix():
    # Global variables.
    global F

    # Get all points selected by the user.
    points = np.asarray(queue, dtype=np.float32)
    
    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->
    split = stereo.shape[1] / 2
    img1 = stereo[:,split:]
    img2 = stereo[:,:split]
    points1 = points[::2]
    points2 = points[1::2]
    F, mask = cv2.findFundamentalMat(points1, points2)
    
    img1_epilined = drawlines(img1, points1, F, (255,0,0))
    img2_epilined = drawlines(img2, points2, F.T, (0,0,255))
    
    plt.subplot(121),plt.imshow(img1_epilined)
    plt.subplot(122),plt.imshow(img2_epilined)
    plt.show()
    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->

def drawlines(img1, points, f1, color):
    ''' img1 - image on which we draw the epilines
        lines - corresponding epilines '''
    r,c = img1.shape[:2]
    img1 = cv2.cvtColor(img1,cv2.COLOR_RGB2BGR)
    
    for point in points:
        line = np.dot(f1, point)
        x0, y0 = map(int, [0, -line[2]/line[1] ])
        x1, y1 = map(int, [c, (line[2]+line[0]*c)/(-line[1]) ])
        img1 = cv2.line(img1, (x0,y0), (x1,y1), color,1)
        
    return img1

########################################################################
# Create a capture video object.
# Tips: You can add a new video capture device or video file with the method
# CaptureVideo.addInputVideo().
capture = CaptureVideo(isDebugging=True)
capture.addInputVideo(2, size=(640, 480), framerate=30.)
capture.addInputVideo(1, size=(640, 480), framerate=30.)

# Creates a window to show the stereo images.
cv2.namedWindow("Stereo", cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback("Stereo", eyeMouseEvent)

# Global variables.
queue  = deque(maxlen=16)
stereo = np.zeros((1, 1, 3), np.uint8)
F      = np.zeros((3, 3)) # <= Create the Fundamental Matrix here.

# This repetion will run while there is a new frame in the video file or
# while the user do not press the "q" (quit) keyboard button.
isFrozen = False
while True:
    # Capture frame-by-frame.
    if not isFrozen:
        retval, frames = capture.getFrames()

        # Check if there is a valid frame.
        if not retval:
            break

        # Create the stereo image.
        stereo = np.hstack((frames[0], frames[1]))

    # Check what the user wants to do.
    key = cv2.waitKey(1)

    # Esc or letter "q" key.
    if key == 27 or key == ord("q"):
        break
    # Letter "f" key.
    elif key == ord("f"):
        isFrozen = not isFrozen
    # Letter "c" key.
    elif key == ord("c"):
        queue.clear()
        F = np.zeros((3, 3))
        isFrozen = False

    # Display the resulting frame.
    cv2.imshow("Stereo", stereo)

# When everything done, release the capture object.
del capture
cv2.destroyAllWindows()
