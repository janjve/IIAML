#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : stereoCameras.py                                         -->
#<!-- Description: Script to work with stereo cameras setups                -->
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

from collections import deque

from CaptureVideo.CaptureVideo import CaptureVideo

########################################################################
def findChessboardCorners(image):
    """Finds the positions of internal corners of the chessboard."""
    # Processed image
    gray = image.copy()

    # Finds the positions of internal corners of the chessboard.
    flags = cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_NORMALIZE_IMAGE | cv2.CALIB_CB_FAST_CHECK
    retval, corners = cv2.findChessboardCorners(gray, (9, 6), flags=flags)

    if retval:
        # Check if the input image is a grayscale image.
        if len(gray.shape) == 3:
            gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

        # Refines the corner locations.
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # Draw the detected chessboard.
        cv2.drawChessboardCorners(image, (9, 6), corners, True)
    else:
        corners = None

    # Garbage Collector.
    del gray

    # Return the final result.
    return corners

def calculatePattern():
    """Creates a standard vectors of the calibration pattern points."""
    # Create the main vector.
    square_size  = 1.0
    objectPoints = np.zeros((np.prod((9, 6)), 3), np.float32)
    objectPoints[:, :2] = np.indices((9, 6)).T.reshape(-1, 2)
    objectPoints *= square_size

    # Return the final result.
    return objectPoints

def calc_matrices(tvecs1, rvecs1, cameraMatrix1, cameraMatrix2):
    skew_symmetric_matrix1 = crossProductMatrix(tvecs1) # This is not correct...
    essential_matrix = skew_symmetric_matrix1 * np.matrix(cv2.Rodrigues(np.array(rvecs1))[0]) # A_x * R

    fundamental_matrix = np.matrix(cameraMatrix2).T.I * essential_matrix * np.matrix(cameraMatrix1).I # K2^-T * E * K1^-1    
    print essential_matrix
    print fundamental_matrix    

def calibrate(leftCorners, rightCorners, objectPoints):
    # Global variables.
    global map1
    global map2

    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->
    use_library_functions = True
    compare = False
    
    cameraMatrix_l = np.zeros((3,3))
    distCoeffs_l = np.zeros((5,1))    
    cameraMatrix_r = np.zeros((3,3))
    distCoeffs_r = np.zeros((5,1))
    
    if not use_library_functions or compare:
        # Using approach from exercise sheet (b), (d), (e)
        retval1, cameraMatrix1, distCoeffs1, rvecs1, tvecs1 = cv2.calibrateCamera(objectPoints, leftCorners, imageSize, cameraMatrix_l, distCoeffs_l)
        retval2, cameraMatrix2, distCoeffs2, rvecs2, tvecs2 = cv2.calibrateCamera(objectPoints, rightCorners, imageSize, cameraMatrix_r, distCoeffs_r)
        
        
        print "VEC1"
        for (i, rvec, tvec) in zip(range(len(rvecs2)), rvecs2, tvecs2):
            print "no: ", str(i)
            calc_matrices(rvec, tvec, cameraMatrix1, cameraMatrix2)
        
        """
        skew_symmetric_matrix1 = crossProductMatrix(tvecs1[0]) # This is not correct...
        essential_matrix = skew_symmetric_matrix1 * np.matrix(cv2.Rodrigues(np.array(rvecs1[0]))[0]) # A_x * R
        
        fundamental_matrix = np.matrix(cameraMatrix2).T.I * essential_matrix * np.matrix(cameraMatrix1).I # K2^-T * E * K1^-1
        print "Manuel"
        print essential_matrix
        print fundamental_matrix
        """
        
    if use_library_functions or compare:
        # Using OpenCV (f), (g), (h)
        retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(objectPoints, leftCorners, rightCorners, 
                           cameraMatrix_l, distCoeffs_l, 
                           cameraMatrix_r, distCoeffs_r, 
                           imageSize)
        print "CV2"
        print E
        print F
        R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, 
                         imageSize, R, T, alpha=0)
        
        map1 = cv2.initUndistortRectifyMap(cameraMatrix1, distCoeffs1, R1, P1, 
                                                     imageSize, cv2.CV_16SC2)
        map2 = cv2.initUndistortRectifyMap(cameraMatrix2, distCoeffs2, R2, P2, 
                                                     imageSize, cv2.CV_16SC2)

        #map1 = map1
        #map2 = map2
    
    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->

def crossProductMatrix(t):
    """Estimating the skew symmetric matrix."""
    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->
    # Calculate cross product matrix (c)
    return np.matrix([[0, -t[2], t[1]], 
                     [t[2], 0, -t[0]],
                     [-t[1], t[0], 0]])

    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->

########################################################################
# Create a capture video object.
# Tips: You can add a new video capture device or video file with the method
# CaptureVideo.addInputVideo().
capture = CaptureVideo(isDebugging=True)
capture.addInputVideo(2, size=(640, 480), framerate=30.)
capture.addInputVideo(1, size=(640, 480), framerate=30.)

# Creates a window to show the stereo images.
cv2.namedWindow("Stereo", cv2.WINDOW_AUTOSIZE)
print "WARNING: When the chessboard will be detected, press \"S\" in your keyboard.\n"

# Global variables.
leftCorners  = []
rightCorners = []
objectPoints = []
imageSize    = (0, 0)
map1 = []
map2 = []

# This repetion will run while there is a new frame in the video file or
# while the user do not press the "q" (quit) keyboard button.
while True:
    # Capture frame-by-frame.
    retval, frames = capture.getFrames()

    # Check if there is a valid frame.
    if not retval:
        break

    # Get the image size.
    imageSize = frames[0].shape[::-1][1:3]

    # Find the pattern in both images.
    left  = findChessboardCorners(frames[0])
    right = findChessboardCorners(frames[1])

    # Create the stereo image.
    stereo = np.hstack((frames[0], frames[1]))

    # Undistorted image.
    if (len(map1) == 2):
        left = cv2.remap(frames[0], map1[0], map1[1], cv2.INTER_LINEAR)
        right = cv2.remap(frames[1], map2[0], map2[1], cv2.INTER_LINEAR)
        undistorted = np.hstack((left, right))
        stereo = np.vstack((stereo, undistorted))
        stereo = cv2.resize(stereo, (0, 0), fx=0.5, fy=0.5)

    # Check what the user wants to do.
    key = cv2.waitKey(1)

    # Esc or letter "q" key.
    if key == 27 or key == ord("q"):
        break

    # Letter "s" key.
    elif key == ord("s"):
        if left is not None and right is not None:
            leftCorners.append(left)
            rightCorners.append(right)
            objectPoints.append(calculatePattern())

            size = len(leftCorners)
            print "Detected Chessboard: %02d of 15." % (size)
            if size == 5:
                calibrate(leftCorners, rightCorners, objectPoints)
                leftCorners  = []
                rightCorners = []
                objectPoints = []

    # Letter "w" key.
    elif key == ord("w"):
        if (len(map1) == 2):
            cv2.imwrite("left.jpg", left)
            cv2.imwrite("right.jpg", right)

    # Letter "c" key.
    elif key == ord("c"):
        leftCorners  = []
        rightCorners = []
        objectPoints = []
        map1 = []
        map2 = []

    # Display the resulting frame.
    cv2.imshow("Stereo", stereo)

# When everything done, release the capture object.
del capture
cv2.destroyAllWindows()
