#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex03_video.py                                            -->
#<!-- Description: Script to capture a video fom a webcam and save each     -->
#<!--            : frame in a JPEG file                                     -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kopenhagen S.   -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 02/02/2016                                               -->
#<!-- Change     : 02/02/2016 - Development of this exercise                -->
#<!-- Review     : 02/02/2017 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2017020201 $"

########################################################################
import numpy as np
import cv2

########################################################################

#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->

# Create a video capture object to capture from video files, image sequences or cameras.
# A
#cap = cv2.VideoCapture("Assets/Field.mp4")
cap = cv2.VideoCapture(1)
# B
'''
cap = cv2.VideoCapture(0)
'''

#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->

# Change the status of saving a video sequence.
is_saving = False
i = 0

# Grab a new frame while the user does not press the "q" button.
while(True):

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow("video", frame)
    key = cv2.waitKey(1)

    # Check the button pressed by the user
    if key == ord("q"):
        break

    if key == ord("s"):
        is_saving = not is_saving

    if is_saving:
        cv2.imwrite("Output/frame_%s.png" % i, gray)
        i += 1
    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
