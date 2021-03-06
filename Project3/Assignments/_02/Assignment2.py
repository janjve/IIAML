#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--           SIGB - Introduction to Graphics and Image Analysis          -->
#<!-- File       : Assignment2.py                                           -->
#<!-- Description: Main class of Assignment #02                             -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D06 - DK-2300 - Copenhagen S    -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 24/10/2015                                               -->
#<!-- Change     : 24/10/2015 - Creation of this class                      -->
#<!-- Review     : 29/03/2016 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2016032901 $"

########################################################################
import cv2
import os
import numpy as np
import warnings

from pylab import draw
from pylab import figure
from pylab import plot
from pylab import show
from pylab import subplot
from pylab import title

import SIGBTools

########################################################################
class Assignment2(object):
    """Assignment2 class is the main class of Assignment #02."""

    #----------------------------------------------------------------------#
    #                           Class Attributes                           #
    #----------------------------------------------------------------------#
    __path = "./Assignments/_02/"

    #----------------------------------------------------------------------#
    #                    Assignment2 Class Constructor                     #
    #----------------------------------------------------------------------#
    def __init__(self):
        """Assignment2 Class Constructor."""
        warnings.simplefilter("ignore")

    #----------------------------------------------------------------------#
    #                         Public Class Methods                         #
    #----------------------------------------------------------------------#
    def Start(self):
        """Start Assignment #02."""
        option = "-1"
        clear  = lambda: os.system("cls" if os.name == "nt" else "clear")
        while option != "0":
            clear()
            print "\n\t#################################################################"
            print "\t#                                                               #"
            print "\t#                         Assignment #02                        #"
            print "\t#                                                               #"
            print "\t#################################################################\n"
            print "\t[1] Person Map Location."
            print "\t[2] Linear Texture Mapping (Ground Floor)."
            print "\t[3] Linear Texture Mapping (Moving Objects)."
            print "\t[4] Linear Texture Mapping (Ensuring a Correctly Placed Texture Map)."
            print "\t[5] Image Augmentation on Image Reality."
            print "\t[6] Camera Calibration."
            print "\t[7] Augmentation."
            print "\t[8] Example \"ShowImageAndPlot()\" method."
            print "\t[9] Example \"SimpleTextureMap()\" method."
            print "\t[0] Back.\n"
            option = raw_input("\tSelect an option: ")

            if option == "1":
                self.__ShowFloorTrackingData()
            elif option == "2":
                self.__TextureMapGroundFloor()
            elif option == "3":
                self.__TextureMapGridSequence()
            elif option == "4":
                self.__RealisticTextureMap()
            elif option == "5":
                self.__TextureMapObjectSequence()
            elif option == "6":
                self.__CalibrateCamera()
            elif option == "7":
                self.__Augmentation()
            elif option == "8":
                self.__ShowImageAndPlot()
            elif option == "9":
                self.__SimpleTextureMap()
            elif option != "0":
                raw_input("\n\tINVALID OPTION!!!")

    #----------------------------------------------------------------------#
    #                        Private Class Methods                         #
    #----------------------------------------------------------------------#
    def __ShowFloorTrackingData(self):
        # Load videodata.
        filename = self.__path + "Videos/ITUStudent.avi"
        image2 = cv2.imread(self.__path + "Images/ITUMap.png")
        SIGBTools.VideoCapture(filename, SIGBTools.CAMERA_VIDEOCAPTURE_640X480)
        SIGBTools.RecordingVideos("C:\\Code\\IIAML\\Project3\\Assignments\\_02\\Outputs\\MapLocation.wmv")
        
        # Load homography
        homography = np.load(self.__path + "Outputs/homography1.npy")
        
        # Load tracking data.
        dataFile = np.loadtxt(self.__path + "Inputs/trackingdata.dat")
        lenght   = dataFile.shape[0]

        # Define the boxes colors.
        boxColors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)] # BGR.

        # Read each frame from input video and draw the rectangules on it.
        for i in range(lenght):
            # Read the current image from a video file.
            image = SIGBTools.read()

            # Draw each color rectangule in the image.
            boxes = SIGBTools.FrameTrackingData2BoxData(dataFile[i, :])
            for j in range(3):
                box = boxes[j]
                cv2.rectangle(image, box[0], box[1], boxColors[j])

            point2 = self.__calcHomogenousCoordinates(boxes[2][1], homography)
            # Show the final processed image.
            # Live tracking
            image2_updated = image2.copy()
            cv2.circle(image2_updated, (int(point2[0]), int(point2[1])), 10, (0, 255, 0), -1)
            cv2.imshow("Map", image2_updated)
            # Drawing
            #cv2.circle(image2, (int(point2[0]), int(point2[1])), 3, (0, 255, 0), -1)
            #cv2.imshow("Map", image2)
            
            cv2.imshow("Ground Floor", image)
            SIGBTools.write(image2_updated)
            
            #self.__showPointsOnFrameOfView(image, points)            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Wait 2 seconds before finishing the method.
        SIGBTools.close()
        cv2.waitKey(2000)
        cv2.imwrite(self.__path + "Outputs/mapImage.png", image2)

        # Close all allocated resources.
        cv2.destroyAllWindows()
        SIGBTools.release()
        
    def __calcHomogenousCoordinates(self, point, homography):
        homogenenous_coordinate = np.append(point, [1])
        point2 = (np.dot(homography, homogenenous_coordinate))
        return point2[:2] / point2[2]        
        
    def __TextureMapGroundFloor(self):
        """Places a texture on the ground floor for each input image."""
        # Load videodata.
        filename = self.__path + "Videos/ITUStudent.avi"
        SIGBTools.VideoCapture(filename, SIGBTools.CAMERA_VIDEOCAPTURE_640X480)
        
        # Needs full path
        SIGBTools.RecordingVideos("C:\\Code\IIAML\\Project3\\Assignments\\_02\\Outputs\\TextureMapGroundFloor.wmv")
        
        # ======================================================
        # Read homography from ground to map.
        H_g2m = np.load(self.__path + "Outputs/homography1.npy")
        
        # Read the input images.
        image1 = cv2.imread(self.__path + "Images/ITULogo.PNG")
        image2 = cv2.imread(self.__path + "Images/ITUMap.png")
        
        # Estimate the homography from image to map.
        H_i2m, points = SIGBTools.GetHomographyFromMouse(image1, image2, -4)
        
        # Calculate homography from image to ground.
        H_i2g = np.dot(np.linalg.inv(H_g2m), H_i2m)
        
        np.save(self.__path + "Outputs/homography2.npy", H_i2g)
        # ========================================================
        
        # Load tracking data.
        dataFile = np.loadtxt(self.__path + "Inputs/trackingdata.dat")
        lenght   = dataFile.shape[0]

        # Define the boxes colors.
        boxColors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)] # BGR.
        images = []
        
        # Read each frame from input video and draw the rectangules on it.
        for i in range(lenght):
            # Read the current image from a video file.
            image = SIGBTools.read()

            # Draw each color rectangule in the image.
            boxes = SIGBTools.FrameTrackingData2BoxData(dataFile[i, :])
            for j in range(3):
                box = boxes[j]
                cv2.rectangle(image, box[0], box[1], boxColors[j])
            
            
            # ========================================================
            # Draw the homography transformation.
            h, w    = image.shape[0:2]
            overlay = cv2.warpPerspective(image1, H_i2g, (w, h))
            result  = cv2.addWeighted(image, 0.5, overlay, 0.5, 0)
            #images.append(result)
            SIGBTools.write(result)
            # ========================================================

            # Show the final processed image.
            cv2.imshow("Camera", result)
            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        
        
        # Wait 2 seconds before finishing the method.
        cv2.waitKey(2000)
        SIGBTools.close()
        # Close all allocated resources.
        cv2.destroyAllWindows()
        
        SIGBTools.release()

    def __TextureMapGridSequence(self):
        """Skeleton for texturemapping on a video sequence."""
        # Load videodata.
        filename = self.__path + "Videos/Grid01.mp4"
        SIGBTools.VideoCapture(filename, SIGBTools.CAMERA_VIDEOCAPTURE_640X480)

        SIGBTools.RecordingVideos("C:\\ITU programming\\IIAML\\Project3\\Assignments\\_02\\Outputs\\TextureMapGridSequenceGrid01.wmv")

        # Load texture mapping image.
        texture = cv2.imread(self.__path + "Images/ITULogo.png")
        texture = cv2.pyrDown(texture)

        # Define the number and ids of inner corners per a chessboard row and column.
        patternSize = (9, 6)
        idx = [53, 45, 8, 0]

        # Read each frame from input video.
        while True:
            # Read the current image from a video file.
            image = SIGBTools.read()
            # Blurs an image and downsamples it.
            image = cv2.pyrDown(image)

            # Finds the positions of internal corners of the chessboard.
            corners = SIGBTools.FindCorners(image)
            if corners is not None:
                # ====================================================
                # Find corner points image
                corner_points = []
                for i, point in enumerate(corners[idx]):
                    corner_points.append(point[0].astype(int).tolist())
                corner_points = np.array(corner_points)
                
                # Corner points texture
                corner_points_texture = np.array([[0,0], 
                                                  [texture.shape[1]-1,0],
                                                  [0,texture.shape[0]-1],
                                                  [texture.shape[1]-1,texture.shape[0]-1]],
                                                 dtype=int)
                
                # Calculate homography
                H = cv2.findHomography(corner_points_texture, corner_points)[0]
                
                # Draw the homography transformation.
                h, w = image.shape[0:2]
                overlay = cv2.warpPerspective(texture, H, (w, h))
                image  = cv2.addWeighted(image, 1, overlay, 1, 0)
                # ====================================================
            
            # Show the final processed image.
            SIGBTools.write(image)
            cv2.imshow("Image", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Wait 2 seconds before finishing the method.
        SIGBTools.close()
        cv2.waitKey(2000)
        # Close all allocated resources.
        cv2.destroyAllWindows()
        SIGBTools.release()

    def __RealisticTextureMap(self):
        # Load videodata.
        filename = self.__path + "Videos/ITUStudent.avi"
        SIGBTools.VideoCapture(filename, SIGBTools.CAMERA_VIDEOCAPTURE_640X480)

        # Load tracking data.
        dataFile = np.loadtxt(self.__path + "Inputs/trackingdata.dat")
        lenght   = dataFile.shape[0]

        # Define the boxes colors.
        boxColors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)] # BGR.

        # Read each frame from input video and draw the rectangules on it.
        for i in range(lenght):
            # Read the current image from a video file.
            image = SIGBTools.read()

            # Draw each color rectangule in the image.
            boxes = SIGBTools.FrameTrackingData2BoxData(dataFile[i, :])
            for j in range(3):
                box = boxes[j]
                cv2.rectangle(image, box[0], box[1], boxColors[j])

            # Show the final processed image.
            cv2.imshow("Ground Floor", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Wait 2 seconds before finishing the method.
        cv2.waitKey(2000)

        # Close all allocated resources.
        cv2.destroyAllWindows()
        SIGBTools.release()

    def __TextureMapObjectSequence(self):
        """Poor implementation of simple TextureMap."""
        # Load videodata.
        filename = self.__path + "Videos/Scene01.mp4"
        SIGBTools.VideoCapture(filename, SIGBTools.CAMERA_VIDEOCAPTURE_640X480)
        drawContours = True

        # Load texture mapping image.
        texture = cv2.imread(self.__path + "Images/ITULogo.png")

        # Read each frame from input video.
        while True:
            # Jump for each 20 frames in the video.
            for t in range(20):
                # Read the current image from a video file.
                image = SIGBTools.read()

            # Try to detect an object in the input image.
            squares = SIGBTools.DetectPlaneObject(image)

            # Check the corner of detected object.
            for sqr in squares:
                # Do texturemap here!!!!
                # TODO
                pass

            # Draws contours outlines or filled contours.
            if drawContours and len(squares) > 0:
                cv2.drawContours(image, squares, -1, (0, 255, 0), 3)

            # Show the final processed image.
            cv2.imshow("Detection", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Wait 2 seconds before finishing the method.
        cv2.waitKey(2000)

        # Close all allocated resources.
        cv2.destroyAllWindows()
        SIGBTools.release()

    def __CalibrateCamera(self):
        """Main function used for calibrating a common webcam."""
        # Load the camera.
        cameraID = 0
        SIGBTools.VideoCapture(cameraID, SIGBTools.CAMERA_VIDEOCAPTURE_640X480_30FPS)

        # Calibrate the connected camera.
        SIGBTools.calibrate()

        # Close all allocated resources.
        SIGBTools.release()

    def __Augmentation(self):
        """Projects an augmentation object over the chessboard pattern."""
        # Load the camera.
        cameraID = 0
        SIGBTools.VideoCapture(cameraID, SIGBTools.CAMERA_VIDEOCAPTURE_640X480_30FPS)

        # Read each frame from input camera.
        while True:
            # Read the current image from the camera.
            image = SIGBTools.read()

            # Finds the positions of internal corners of the chessboard.
            corners = SIGBTools.FindCorners(image, False)
            if corners is not None:
                pass

            # Show the final processed image.
            cv2.imshow("Augmentation", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Wait 2 seconds before finishing the method.
        cv2.waitKey(2000)

        # Close all allocated resources.
        cv2.destroyAllWindows()
        SIGBTools.release()

    def __ShowImageAndPlot(self):
        """A simple attempt to get mouse inputs and display images using pylab."""
        # Read the input image.
        image = cv2.imread(self.__path + "Images/frame_S.png")
        image2  = cv2.imread(self.__path + "Images/ITUMap.png")

        homography = np.array([[1.38313735e+00, 3.70453015e+00, -5.94765885e+01],
                                   [-8.35013640e-01, 1.13045450e+00, 2.85528598e+02],
                                   [3.25873637e-03, 5.71413156e-03, 1.00000000e+00]])

        # Make figure and two subplots.
        fig = figure(1)
        ax1 = subplot(1, 2, 1)
        ax2 = subplot(1, 2, 2)
        ax1.imshow(image)
        ax2.imshow(image2)
        ax1.axis("image")
        ax1.axis("off")

        # Read 5 points from the input images.
        points = fig.ginput(5)
        fig.hold("on")

        # Draw the selected points in both input images.
        for point in points:
            # Draw on matplotlib.
            subplot(1, 2, 1)
            plot(point[0], point[1], "rx")
            
            point2 = self.__calcHomogenousCoordinates(point, homography)
            # Draw on opencv.
            cv2.circle(image2, (int(point2[0]), int(point2[1])), 10, (0, 255, 0), -1)

        # Clear axis.
        ax2.cla()
        # Show the second subplot.
        ax2.imshow(image2)
        # Update display: updates are usually deferred.
        draw()
        show()
        # Save with matplotlib and opencv.
        fig.savefig(self.__path + "Outputs/imagePyLab.png")
        cv2.imwrite(self.__path + "Outputs/imageOpenCV.png", image2)

    def __SimpleTextureMap(self):
        """Example of how linear texture mapping can be done using OpenCV."""
        # Read the input images.
        image1 = cv2.imread(self.__path + "Images/ITULogo.PNG")
        image2 = cv2.imread(self.__path + "Images/ITUMap.png")
        

        # Estimate the homography.
        H, points = SIGBTools.GetHomographyFromMouse(image1, image2, 4)
        np.save(self.__path + "Outputs/homography1.npy", H)
        
        # Draw the homography transformation.
        h, w    = image2.shape[0:2]
        overlay = cv2.warpPerspective(image1, H, (w, h))
        result  = cv2.addWeighted(image2, 0.5, overlay, 0.5, 0)
        
        # Show the result image.
        cv2.imshow("SimpleTextureMap", result)
        cv2.waitKey(0)

        # Close all allocated resources.
        cv2.destroyAllWindows()
