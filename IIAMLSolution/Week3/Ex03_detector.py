
#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex03_detector.py                                         -->
#<!-- Description: Script to detect objects based on colors in some image   -->
#<!--            : sequences from a video file or a webcam                  -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kopenhagen S.   -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 03/12/2016                                               -->
#<!-- Change     : 03/12/2016 - Development of this exercise                -->
#<!-- Review     : 10/02/2017 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2017021001 $"

########################################################################
import argparse
import cv2
import numpy as np

########################################################################
# Construct the argument parse and parse the arguments.
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="Path to the (optional) video file")
args = vars(ap.parse_args())

# Define the lower and upper boundaries of the HSV pixel
# of the object that you would like to recognize.
lower = np.array([  0, 223, 127], dtype="uint8")
upper = np.array([120, 255, 255], dtype="uint8")

# Load a video camera or a video file.
if not args.get("video", False):
    video = cv2.VideoCapture(0)
else:
    video = cv2.VideoCapture(args["video"])

# Grab each individual frame.
while True:
    # Grabs, decodes and returns the next video frame.
    retval, frame = video.read()

    # Check if there is a valid frame.
    if not retval:
        break
    
    # Preprocessing
    result = cv2.resize(frame, (320, 240))
    result_hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)

    #blue
    mask = cv2.inRange(result_hsv, (0,223,127),(120,255,255))

    result_masked = cv2.bitwise_and(result, result, mask=mask)
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    row1 = np.hstack((result, result_hsv))
    row2 = np.hstack((mask_bgr, result_masked))
    result = np.vstack((row1,row2))

    # Show the processed images.
    cv2.imshow("Result", result)
    
    # Get the keyboard event.
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Closes video file or capturing device.
video.release()

# Destroys all of the HighGUI windows.
cv2.destroyAllWindows()
