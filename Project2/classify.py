# USAGE
# python classify.py --model models/svm.cpickle --image images/umbc_zipcode.png --scene_video images/out_scene.mp4 --eye_video images/out_eye.mp4

# import the necessary packages
from __future__ import print_function
from sklearn.externals import joblib
from DataAndDescription.descriptors import HOG
from DataAndDescription.utils import dataset
from detect_pupil import *
from sklearn import svm
import matplotlib.pyplot as plt
import numpy as np
import argparse
import mahotas
import cv2
import pickle

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True, help="path to where the model will be stored")
ap.add_argument("-i", "--image", required= False, help="path to the image file")
ap.add_argument("-ev", "--eye_video", required= True, help="path to the eye video file")
ap.add_argument("-sv", "--scene_video", required= True, help="path to the scene video file")
args = vars(ap.parse_args())


# --- load calibration matrix
filepath = "CalibrationMatrix/matrix_scenario_1.pkl"
fileStream = open(filepath, "rb")
matrix = pickle.load(fileStream)
fileStream.close()

#--------------------------
# --- create control bars
# -------------------------
def callback(value):
	pass

def setup_roibars(ImageShape):
	cv2.namedWindow("ROIBars", 0)

	cv2.createTrackbar("Left", "ROIBars", 400, ImageShape[1], callback)
	cv2.createTrackbar("Right", "ROIBars", 880, ImageShape[1], callback)    
	cv2.createTrackbar("Up", "ROIBars", 150, ImageShape[0], callback)
	cv2.createTrackbar("Down", "ROIBars", 400, ImageShape[0], callback)
	cv2.createTrackbar("Pause", "ROIBars", 0, 1, callback)

def get_roibar_values():
	values = []

	for i in ["Left", "Right", "Up", "Down", "Pause"]:
		v = cv2.getTrackbarPos("%s" % i, "ROIBars")
		values.append(v)

	return values
def calculate_gaze_point(XMin, YMin, pupilX, pupilY):
	homo_pupil_center = [XMin + pupilX, YMin + pupilY, 1]
	gaze_point = np.dot(matrix, homo_pupil_center)
	gaze_point /= gaze_point[2]
	gaze_point = np.multiply(gaze_point, [1280, 720, 1])
	print (gaze_point)
	return gaze_point

#-------- end create control bars ---

# load the model
model = joblib.load(args["model"])

# initialize the HOG descriptor
hog = HOG(orientations=18, 
          pixelsPerCell=(2, 2), 
          cellsPerBlock=(2, 2), 
          normalize=True)

# load the eye and scene video streams
cap_eye = cv2.VideoCapture(args["eye_video"])
cap_scene = cv2.VideoCapture(args["scene_video"])

# Grab first frame of eye and scene videos
ret_eye, eye_image = cap_eye.read()
ret_scene, scene_image = cap_scene.read()

roibarFlag = True
grabFlag = False

while(True):
	# Capture frame-by-frame
	if grabFlag:
		ret_eye, eye_image = cap_eye.read()
		ret_scene, scene_image = cap_scene.read()
	# create roibars to define ROI
	if roibarFlag:
		setup_roibars(eye_image.shape[:2])
		roibarFlag = False    

	# draw ROI lines
	XMin, XMax, YMin, YMax, grabFlag = get_roibar_values()

	# draw ROI
	result = eye_image.copy()
	cv2.line(result, (XMin, 0), (XMin, result.shape[0]), [255,255,255], thickness=1)
	cv2.line(result, (XMax, 0), (XMax, result.shape[0]), [255,255,255], thickness=1)
	cv2.line(result, (0, YMin), (result.shape[1], YMin), [255,255,255], thickness=1)
	cv2.line(result, (0, YMax), (result.shape[1], YMax), [255,255,255], thickness=1)	

	if grabFlag:
		# crop image
		#print eye_image
		cropped_frame = eye_image[YMin:YMax, XMin:XMax]
		#print cropped_frame
		pupilX , pupilY = DetectPupil(cropped_frame)
		cv2.circle(eye_image, (XMin + int(pupilX), YMin + int(pupilY)), 5, (0, 255, 0), 1)
		cv2.circle(cropped_frame, (int(pupilX), int(pupilY)), 3, (0, 0, 255), -1)
		
		# estimate gaze point in the scene video
		gaze_point = calculate_gaze_point(XMin, YMin, pupilX, pupilY)
		
		# Convert scene image to grayscale
		gray = cv2.cvtColor(scene_image, cv2.COLOR_BGR2GRAY)
		
		# blur the image, find edges, and then find contours along the edged regions
		blurred = cv2.GaussianBlur(gray, (5, 5), 0)
		edged = cv2.Canny(blurred, 30, 150)
		#cv2.imshow("a", edged)
		#cv2.waitKey(0)
		(_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		
		# sort the contours by their x-axis position, ensuring that we read the numbers from
		# left to right
		cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in cnts], key=lambda x: x[1])
		
		# loop over the contours
		for (c, _) in cnts:
			# compute the bounding box for the rectangle
			(x, y, w, h) = cv2.boundingRect(c)
		
			# if the width is at least 7 pixels and the height is at least 20 pixels, the contour
			# is likely a digit
			if w >= 7 and w < 250 and h >= 60 and h < 250:
				# crop the ROI and then threshold the grayscale ROI to reveal the digit
				roi = gray[y:y + h, x:x + w]
				thresh = roi.copy()
				T = mahotas.thresholding.otsu(roi)
				thresh[thresh > T] = 255
				thresh = cv2.bitwise_not(thresh)
		
				# deskew the image center its extent
				thresh = dataset.deskew(thresh, 28)
				thresh = dataset.center_extent(thresh, (28, 28))
		
				#<------------------------------------------------------------>
				#<---------- Describe HOG features and Classify Digit -------->
				#<------------------------------------------------------------>				
				
				# extract features from the image and classify it
				
				
				#hist = hog.describe(thresh)
				flattened = np.array([thresh.flatten()])
				prediction = model.predict(flattened)
				
				
				# draw a rectangle around the digit, the show what the digit was classified as
				is_candidate = False
				if prediction[0] == 1 and h / w > 3:
					is_candidate = True
				elif h / w > 0.4 and h / w < 2.5:
					is_candidate = True
				if is_candidate:
					error_calibrated_w = w * 0.3 # gaze_error_tolerence_w
					error_calibrated_h = h * 0.3 # gaze_error_tolerence_h
					if gaze_point[0] > x - error_calibrated_w and gaze_point[0] < x + w + error_calibrated_w and gaze_point[1] > y - error_calibrated_h and gaze_point[1] < y + h + error_calibrated_h:
						cv2.rectangle(scene_image, (x,y), (x+w,y+h), (0,255,0), 2)
						cv2.putText(scene_image, str(prediction[0]), (x,y), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0))
					else:
						cv2.rectangle(scene_image, (x,y), (x+w,y+h), (0,0,255))					
						
				
				#<------------------------------------------------------------>
				#<                                                            >
				#<------------------------------------------------------------>				
				
		
		cv2.circle(scene_image, (int(gaze_point[0]), int(gaze_point[1])), 15, (255, 0, 0), -1)
	if not grabFlag:
		cv2.imshow("Full Eye Frame", result)
	if grabFlag:
		cv2.imshow("Cropped Eye Frame", cropped_frame)
		cv2.imshow("Full Eye Frame", eye_image)
	cv2.imshow("Detected Digits", scene_image)
	cv2.waitKey(1)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
		