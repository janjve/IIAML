#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex04_rotations.py                                        -->
#<!-- Description: Script to introduce planar geometric transformations     -->
#<!--            : (rotation and translation), some properties of matrices, -->
#<!--            : and homogeneous and Euclidean representations            -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kopenhagen S.   -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 08/12/2016                                               -->
#<!-- Change     : 08/12/2016 - Development of this exercise                -->
#<!-- Review     : 17/02/2017 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2017021701 $"

########################################################################
import math
import matplotlib.pyplot as plt
import numpy as np

########################################################################
def showPoints(points, color="black", title="Rotations"):
    """This function creates a Matplotlib window and shows four histograms."""
    plt.title(title)
    plt.xlabel("X-Axis")
    plt.xlim([-10, 10])
    plt.ylabel("Y-Axis")
    plt.ylim([-10, 10])
    plt.plot(points[0, :], points[1, :], 'o', color=color)

def rotate2D(theta):
    """
    This function return a rotation matrix given an input theta angle in
    radians.
    """
    #<!--------------------------------------------------------------------------->
    #<!--                            YOUR CODE HERE                             -->
    #<!--------------------------------------------------------------------------->

    return np.matrix([[math.cos(theta), -math.sin(theta)],
                     [math.sin(theta), math.cos(theta)]], dtype=np.float64)

    #<!--------------------------------------------------------------------------->
    #<!--                                                                       -->
    #<!--------------------------------------------------------------------------->

def transformation(theta=0, t=(0, 0)):
    """
    This function return a 3x3 homogeneous transformation matrix that
    represents a rotation followed by a translation transformation.    """
    return np.array([[ math.cos(theta), -math.sin(theta), t[0] ],
                     [ math.sin(theta),  math.cos(theta), t[1] ],
                     [               0,                0,   1  ]],
                    dtype=np.float64)

def toHomogeneous(points):
    """
    This function convert Euclidean coordinates points in homogeneous
    coordinates points.    """
    return np.vstack((points, np.ones((1, points.shape[1]))))

def toEuclidean(points):
    """
    This function convert homogeneous coordinates points in Euclidean
    coordinates points.    """
    for point in points:
        point /= point[2]

    return point[:2]

#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->
# Exercise 4.02.b, c

angle = math.pi * 2.1
R = rotate2D(angle)
point = np.array([[0], 
                  [1]], dtype = np.float64)
p = R * point
"""
print p
"""

# Exercise 4.02.d
P1 = np.array([[0,  1, -1, -1], 
               [1, -1, -1,  1]], dtype = np.float64)
P1_ = R * P1

#"""
showPoints(P1, color = '0.75')
showPoints(P1_)
#"""

# Exercise 4.02.e
P2 = np.array([[3,  3, 2, 2], 
               [3, -2, 2, 3]], dtype = np.float64)
P2_ = R * P2

#"""
showPoints(P2, color = 'red')
showPoints(P2_, color = 'magenta')
#"""
plt.show()
#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->
print ""
raw_input("Done. Press enter to terminate..")