#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : EyeFeatureDetector.py                                    -->
#<!-- Description: Class used for detecting some eye feature (e.g. pupil,   -->
#<!--            : glints, iris, among others) from the input videos        -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kobenhavn S.    -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 13/02/2017                                               -->
#<!-- Change     : 13/02/2017 - Creation of these classes                   -->
#<!-- Review     : 13/02/2017 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2017021301 $"

########################################################################
import cv2
import math
import matplotlib.pyplot as plt
import numpy as np

from GeometricMethods import *
from RegionProps import RegionProps

########################################################################
class EyeFeatureDetector(object):
    """
    Class used for detecting some eye feature (e.g. pupil, glints, iris, among
    others) from the input videos.
    """

    #----------------------------------------------------------------------#
    #                           Class Properties                           #
    #----------------------------------------------------------------------#
    @property
    def Props(self):
        """Get a descriptors of contour-based connected components."""
        return self.__Props

    #----------------------------------------------------------------------#
    #                 EyeFeatureDetector Class Constructor                 #
    #----------------------------------------------------------------------#
    def __init__(self):
        """EyeFeatureDetector Class Constructor."""
        self.__Props = RegionProps()
        self.__firstPlot = True

    def __del__(self):
        """EyeFeatureDetector Class Destructor."""
        pass

    #----------------------------------------------------------------------#
    #                   Incomplete Public Class Methods                    #
    #----------------------------------------------------------------------#
    def getPupil(self, image, threshold=0, pupilMinimum=10, pupilMaximum=50):
        """
        Given an image, return the coordinates of the pupil candidates.
        """
        # Create the output variable.
        bestPupil = -1
        bestProps = {}
        ellipses  = []
        centers   = []

        # Create variables to plot the regression data.
        # TIPS: You must select two blob properties and add their values in
        #       the following lists. Then, call the private method
        #       __plotData() in the end of your implementation.
        x = []
        y = []

        # Grayscale image.
        grayscale = image.copy()
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
        #_, thres = cv2.threshold(grayscale, threshold, 255,
        #                         cv2.THRESH_BINARY_INV)
        thres = self.__GetAutoThreshold(grayscale)
        
        #print thres
        # Find blobs in the input image.
        _, contours, hierarchy = cv2.findContours(thres, cv2.RETR_LIST,
                                                  cv2.CHAIN_APPROX_SIMPLE)

        #<!--------------------------------------------------------------------------->
        #<!--                            YOUR CODE HERE                             -->
        #<!--------------------------------------------------------------------------->
        for blob in contours:
            props = self.Props.calcContourProperties(blob,["centroid", "area", "extend", "circularity"])
                
            # Is candidate
            if 1000.0 < props["Area"] and props["Area"] < 8000.0 and 0.65 < props["Extend"] and props["Extend"] < 0.9 and props["Circularity"] > 0.4:
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
        
        #self.__plotData(x, y, bestPupil)
        #<!--------------------------------------------------------------------------->
        #<!--                                                                       -->
        #<!--------------------------------------------------------------------------->

        # Return the final result.
        return ellipses, centers, bestPupil

    def getGlints(self, image, threshold=0, glintsMinimum=1, glintsMaximum=10,
                  numOfGlints=1, pupilCenter=(0, 0)):
        """
        Given an image, return the coordinates of the glints candidates.
        """
        # Correct the number of glints.
        if numOfGlints < 1:
            numOfGlints = 1

        # Create the output variable.
        bestGlints = [-1] * numOfGlints
        bestGlintsProps = [{}] * numOfGlints
        ellipses  = []
        centers   = []
        
        grayscale = image.copy()
        if len(grayscale.shape) == 3:
            grayscale = cv2.cvtColor(grayscale, cv2.COLOR_BGR2GRAY)    
            
        glintProps = []

        #_, thres = cv2.threshold(grayscale, threshold, 255,cv2.THRESH_BINARY_INV)
        thres =  self.__GetAutoThresholdGlints(grayscale)

        # Find blobs in the input image.
        _, contours, hierarchy = cv2.findContours(thres, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        pupilCenterAsNumpyArray = np.array(pupilCenter)
        for blob in contours:
            props = self.Props.calcContourProperties(blob, ["centroid", "area", "extend", "circularity"])
<<<<<<< HEAD
            if props["Area"] < 700.0 and props["Area"]>20 and props["Circularity"] > 0.2:
=======
            distance = np.linalg.norm(np.array(props["Centroid"]) - pupilCenterAsNumpyArray)
            if props["Area"] < 350.0 and props["Circularity"] > 0.2 and distance < 100:
>>>>>>> origin/master
                centers.append(props["Centroid"])
                glintProps.append(props)
                if len(blob) > 4:
                        ellipses.append(cv2.fitEllipse(blob))
                else:
                        ellipses.append(cv2.minAreaRect(blob))
        
        i = 0
        if len(ellipses) <= numOfGlints:
            for ell in ellipses:
                bestGlints[i] = i
                i += 1
        else:
            bestGlints = self.__GetBestGlints(glintProps, pupilCenterAsNumpyArray, numOfGlints)
        print i
        #<!--------------------------------------------------------------------------->
        #<!--                                                                       -->
        #<!--------------------------------------------------------------------------->

        # Return the final result.
        return ellipses, centers, bestGlints
    
    def getIris(self, image, pupilCenter, pupilRadius, numOfPoints=120):
        """
        Given an image, return the coordinates of the iris candidates.
        """
        # Create the output variable.
        lines = []
        points = []
        ellipse = None
        # Get the gradient info from the input image.
        gradient, orientation, magnitude = self.__GetGradientInfo(image)

        # Get the points distribuition around one circle.
        circle = getCircleSamples(pupilCenter, pupilRadius, numOfPoints)
        
        #<!--------------------------------------------------------------------------->
        #<!--                            YOUR CODE HERE                             -->
        #<!--------------------------------------------------------------------------->
        for (center, dx, dy) in circle:
            maxDistance = 150
            p1 = center
            p2 = (pupilCenter[0] + dx * maxDistance, pupilCenter[1] + dy * maxDistance)
            maxPoint = self.__FindMaxGradientValueOnNormal(magnitude, orientation, p1, p2)
            
            if not (maxPoint[0] == 0 and maxPoint[1] == 0):
                points.append(maxPoint)

        ellipse = cv2.fitEllipse(np.array(points))
        #<!--------------------------------------------------------------------------->
        #<!--                                                                       -->
        #<!--------------------------------------------------------------------------->

        return ellipse, lines, points

    #----------------------------------------------------------------------#
    #                         Public Class Methods                         #
    #----------------------------------------------------------------------#
    def getProcessedImage(self, image, threshold, pupilsEllipses=None,
                          pupilsCenters=None, bestPupil=None,
                          glintsEllipses=None, glintsCenters=None,
                          bestGlints=None, irisEllipse=None,
                          irisLines=None, irisPoints=None):
        """"
        Given an image and some eye feature coordinates, return the processed
        image.
        """
        # Create the output variable
        processed = np.zeros(image.shape, np.uint8)

        # Baseline image and image resolution.
        result = image.copy()
        height, width = image.shape[:2]

        # Copy the original image for the first position.
        processed[:height/2, :width/2, :] = cv2.resize(result,
                                                       (width/2, height/2))

        # Copy the threshold image for the second position.
        grayscale = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        
        if glintsEllipses == None and irisEllipse == None:        
            thres =self.__GetAutoThreshold(grayscale)            
            #_, thres = cv2.threshold(grayscale, threshold, 255, cv2.THRESH_BINARY_INV)
        elif irisEllipse == None:
            #_, thres = cv2.threshold(grayscale, threshold, 255, cv2.THRESH_BINARY)
            thres =  self.__GetAutoThresholdGlints(grayscale)
        else:
            thres = self.__GetSobel(grayscale)

        thres = cv2.cvtColor(thres, cv2.COLOR_GRAY2BGR)
        processed[:height/2, width/2:, :] = cv2.resize(thres,
                                                       (width/2, height/2))

        # Copy all candidates to the third position.
        candidates = result.copy()

        if (pupilsEllipses != None and len(pupilsEllipses) > 0 and
            pupilsCenters  != None and len(pupilsCenters) > 0):
            for pupil, center in zip(pupilsEllipses, pupilsCenters):
                self.__DrawCenter(candidates, center, (0, 0, 255))
                self.__DrawEllipse(candidates, pupil, (0, 0, 255))

        if (glintsEllipses != None and len(glintsEllipses) > 0 and
            glintsCenters  != None and len(glintsCenters) > 0):
            for glint, center in zip(glintsEllipses, glintsCenters):
                self.__DrawCenter(candidates, center, (0, 255, 0))
                self.__DrawEllipse(candidates, glint, (0, 255, 0))
    
        elif (irisLines != None and irisPoints != None):
            for line, point in zip(irisLines, irisPoints):
                cv2.line(candidates, line[0], line[1], (0, 255, 0), 2)
                cv2.circle(candidates, point, 2, (255, 0, 0), 5)

        processed[height/2:, :width/2, :] = cv2.resize(candidates,
                                                       (width/2, height/2))

        # Copy the best pupil candidate to the fourth position.
        if bestPupil != -1:
            self.__DrawCenter(result, pupilsCenters[bestPupil], (0, 0, 255))
            self.__DrawEllipse(result, pupilsEllipses[bestPupil], (0, 0, 255))

        if bestGlints != None:
            for best in bestGlints:
                if best != -1:
                    self.__DrawCenter(result, glintsCenters[best], (0, 255, 0))
                    self.__DrawEllipse(result, glintsEllipses[best], (0, 255, 0))

        elif irisEllipse != None:
            self.__DrawEllipse(result, irisEllipse, (0, 255, 0))

        processed[height/2:, width/2:, :] = cv2.resize(result,
                                                       (width/2, height/2))

        # Return the final result.
        return processed

    #----------------------------------------------------------------------#
    #                   Incomplete Private Class Methods                   #
    #----------------------------------------------------------------------#
    def __GetBestGlints(self, glintProps, pupilCenter, numOfGlints):
        """Get the Euclidean distance between."""
        #<!--------------------------------------------------------------------------->
        #<!--                            YOUR CODE HERE                             -->
        #<!--------------------------------------------------------------------------->
        bestGlints = [-1] * numOfGlints
        bestGlintsProps = [{}] * numOfGlints
        
        pupilCenterAsNumpyArray = np.array(pupilCenter)
        # Filling bestGlints
        if not glintProps == []:
            for center in xrange(len(glintProps)): 
                glintCount = len([x for x in bestGlints if x > -1])
                if(glintCount < numOfGlints):
                    bestGlints[glintCount] = center
                    bestGlintsProps[glintCount] = glintProps[center]
                
        for i in xrange(len(glintProps)):
            glintCount = len([x for x in bestGlints if x > -1])
            worst = -1
            # Find the worst of the best glints.
            for current in xrange(glintCount):
                if worst == -1 or np.linalg.norm(np.array(bestGlintsProps[current]["Centroid"]) - pupilCenterAsNumpyArray) > np.linalg.norm(np.array(bestGlintsProps[worst]["Centroid"]) - pupilCenterAsNumpyArray):
                    worst = current
                    
            # Compare current blob with the worst glint.
            if np.linalg.norm(np.array(glintProps[i]["Centroid"]) - pupilCenterAsNumpyArray) < np.linalg.norm(np.array(bestGlintsProps[worst]["Centroid"]) - pupilCenterAsNumpyArray):
                bestGlints[worst] = i
                bestGlintsProps[worst] = glintProps[i]
                
        return bestGlints

        #<!--------------------------------------------------------------------------->
        #<!--                                                                       -->
        #<!--------------------------------------------------------------------------->

    def __FindMaxGradientValueOnNormal(self, magnitude, orientation, p1, p2):
        """
        Find the boundary of the iris using the maximum gradient magnitude
        along the normals.
        """
        # Create the output variable.
        maxPoint = (0, 0)

        # Get integer coordinates on the straight line between p1 and p2.
        points = getLineCoordinates(p1, p2)
        try:
            normalVals = magnitude[points[:, 1], points[:, 0]]
            normalOri = orientation[points[:, 1], points[:, 0]]
        except:
            return maxPoint
    
        #<!--------------------------------------------------------------------------->
        #<!--                            YOUR CODE HERE                             -->
        #<!--------------------------------------------------------------------------->
        maxVal = -1
        ori1 = np.arctan((p1[0] - p2[0]) / (p1[1] - p2[1])) * 180. / np.pi
        for i in xrange(len(normalVals)):
            if maxVal < normalVals[i]:
                ori2 = normalOri[i]
                if np.abs(ori1 - ori2) < 5:
                    maxVal = normalVals[i]
                    maxPoint = points[i]
        #<!--------------------------------------------------------------------------->
        #<!--                                                                       -->
        #<!--------------------------------------------------------------------------->
        # Return the final result.
        return maxPoint

    def __GetGradientInfo(self, image):
        """
        Get the image gradient, the gradient magnitude and the gradient
        directions from an input image.
        """
        # Create the output variable.
        gradient = [np.zeros(image.shape[:2])] * 2
        orientation = np.zeros(image.shape[:2])
        magnitude = np.zeros(image.shape[:2])

        # Grayscale image.
        grayscale = image.copy()
        if len(grayscale.shape) == 3:
            grayscale = cv2.cvtColor(grayscale, cv2.COLOR_BGR2GRAY)

        #<!--------------------------------------------------------------------------->
        #<!--                            YOUR CODE HERE                             -->
        #<!--------------------------------------------------------------------------->
        gradient = np.gradient(grayscale)
        
        #orientation = np.arctan(gradient[0], gradient[1]) * (180. / np.pi)
        #magnitude = np.sqrt(np.power(gradient[0], 2) + np.power(gradient[1], 2))
        
        magnitude, orientation = cv2.cartToPolar(gradient[0], gradient[1], angleInDegrees=True)
        
        #<!--------------------------------------------------------------------------->
        #<!--                                                                       -->
        #<!--------------------------------------------------------------------------->
        
        # Return the final result.
        return gradient, orientation, magnitude

    #----------------------------------------------------------------------#
    #                        Private Class Methods                         #
    #----------------------------------------------------------------------#
    def __DrawCenter(self, image, center, color):
        """Drawing a cross over a determined region in the processed image."""
        if center[0] != -1 and center[1] != -1:
            cv2.circle(image, (int(center[0]), int(center[1])), 5, color, -1)

    def __DrawEllipse(self, image, rectangule, color):
        """Drawing an ellipse around a detected blob."""
        cv2.ellipse(image, rectangule, color, 2)
        points = cv2.boxPoints(rectangule)
        for i in range(4):
            cv2.line(image, tuple(np.array(points[i], np.int32)),
                     tuple(np.array(points[(i + 1) % 4], np.int32)), color, 2)

    def __GetSobel(self, image):
        """Get the Sobel borders using OpenCV."""
        # Gradient X.
        gradX = cv2.Sobel(image, cv2.CV_64F, 1, 0)

        # Gradient Y.
        gradY = cv2.Sobel(image, cv2.CV_64F, 0, 1)

        # Converting back to uint8 dtype.
        absX = cv2.convertScaleAbs(gradX)
        absY = cv2.convertScaleAbs(gradY)

        # Merge the horizontal and vertical components.
        return cv2.addWeighted(absX, 0.5, absY, 0.5, 0)

    def __plotData(self, x, y, bestPupil):
        """Plot the data based on blob properties."""
        # Check if there are valid data.
        if bestPupil == -1:
            return

        # Check if the user will plot for the first time.
        if self.__firstPlot:
            self.__fig, self.__ax = plt.subplots()
            self.__line, = self.__ax.plot([0, x[bestPupil]], [0, y[bestPupil]], "ko")
            plt.show(block=False)
            self.__firstPlot = False

        # Plot the data.
        self.__line.set_xdata(x)
        self.__line.set_ydata(y)
        self.__ax.plot(x[bestPupil], y[bestPupil], "ro")
        self.__ax.draw_artist(self.__ax.patch)
        self.__ax.draw_artist(self.__line)
        self.__fig.canvas.blit(self.__ax.bbox)
        self.__fig.canvas.flush_events()

    def __GetAutoThreshold(self, grayscale):    
        thres = cv2.adaptiveThreshold(grayscale,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,61,11)        
        return thres
    
    def __GetAutoThresholdGlints(self,grayscale): 
        #thres = cv2.GaussianBlur(grayscale, (19,19), 1)
        #kernel = np.ones((11,11))
        #thres = cv2.morphologyEx(grayscale, cv2.MORPH_CLOSE, kernel)                   
        thres = cv2.adaptiveThreshold(grayscale,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,15,10)    
        kernel = np.ones((2,2))    
        thres = cv2.morphologyEx(thres, cv2.MORPH_ERODE, kernel)         
        kernel = np.ones((10,10))
        thres = cv2.morphologyEx(thres, cv2.MORPH_CLOSE, kernel)        
        return thres        
            
