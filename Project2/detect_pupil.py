# import the necessary packages
import argparse
import imutils
import cv2
import math
from RegionProps import RegionProps

def DetectPupil(cropped_frame):
    #<------------------------------------------------------------>
    #<---------- Implement your pupil detector here -------------->
    #<------------------------------------------------------------>
    # Create the output variable.
    
    Props = RegionProps()
    
    bestPupil = -1
    bestProps = {}
    ellipses  = []
    centers   = []
    pupilMinimum=10 
    pupilMaximum=50
    # Create variables to plot the regression data.
    # TIPS: You must select two blob properties and add their values in
    #       the following lists. Then, call the private method
    #       __plotData() in the end of your implementation.
    x = []
    y = []

    # Grayscale image.
    grayscale = cropped_frame.copy()
    if len(grayscale.shape) == 3:
        grayscale = cv2.cvtColor(grayscale, cv2.COLOR_BGR2GRAY)

    # Define the minimum and maximum size of the detected blob.
    pupilMinimum = int(round(math.pi * math.pow(pupilMinimum, 2)))
    pupilMaximum = int(round(math.pi * math.pow(pupilMaximum, 2)))

    # Preprocessing
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7))
    grayscale = cv2.morphologyEx(grayscale, cv2.MORPH_OPEN, kernel)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))
    grayscale = cv2.morphologyEx(grayscale, cv2.MORPH_CLOSE, kernel)
    
    # Create a binary image.
    thres = cv2.adaptiveThreshold(grayscale,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,111,20)                              
    
    # Find blobs in the input image.
    _, contours, hierarchy = cv2.findContours(thres, cv2.RETR_LIST,
                                              cv2.CHAIN_APPROX_SIMPLE)

    for blob in contours:
        props = Props.calcContourProperties(blob,["centroid", "area", "extend", "circularity"])
            
        # Is candidate
        if 500.0 < props["Area"] and props["Area"] < 8000.0 and 0.65 < props["Extend"] and props["Extend"] < 0.9 and props["Circularity"] > 0.4:
            centers.append(props["Centroid"])
            if len(blob) > 4:
                ellipses.append(cv2.fitEllipse(blob))
                x.append(props["Area"])
                y.append(props["Extend"])
            else:
                ellipses.append(cv2.minAreaRect(blob))
                x.append(props["Area"])
                y.append(props["Extend"])
            
            # Update best props
            if bestPupil == -1 or props["Circularity"] > bestProps["Circularity"]: # Append other checks.
                bestProps = props
                bestPupil = len(ellipses) - 1
    
    # Return the final result.
    if len(centers):
        return centers[bestPupil]
    else:
        return (0,0) # No pupil candidate found