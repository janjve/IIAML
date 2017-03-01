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
    represents a rotation followed by a translation transformation.
    """
    return np.array([[ math.cos(theta), -math.sin(theta), t[0] ],
                     [ math.sin(theta),  math.cos(theta), t[1] ],
                     [               0,                0,   1  ]],
                    dtype=np.float64)

def toHomogeneous(points):
    """
    This function convert Euclidean coordinates points in homogeneous
    coordinates points.
    """
    return np.vstack((points, np.ones((1, points.shape[1]))))

def toEuclidean(points):
    """
    This function convert homogeneous coordinates points in Euclidean
    coordinates points.
    """
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

"""
showPoints(P1, color = '0.75')
showPoints(P1_)
"""

# Exercise 4.02.e
P2 = np.array([[3,  3, 2, 2], 
               [3, -2, 2, 3]], dtype = np.float64)
P2_ = R * P2

"""
showPoints(P2, color = 'red')
showPoints(P2_, color = 'magenta')
"""

# Exercise 4.02.f
p4 = np.array([[0],
               [0]], dtype=np.float64)
t1 = np.array([[0],
               [1]], dtype=np.float64)
t2 = np.array([[1],
               [0]], dtype=np.float64)
t3 = np.array([[-3],
               [ 4]], dtype=np.float64)
t4 = np.array([[-2],
               [-1]], dtype=np.float64)

p4_t1 = p4 + t1
p4_t2 = p4 + t2
p4_t3 = p4 + t3
p4_t4 = p4 + t4
"""
showPoints(p4)
showPoints(p4_t1, color="red")
showPoints(p4_t2, color="green")
showPoints(p4_t3, color="blue")
showPoints(p4_t4, color="yellow")
"""

# Exercise 4.02.g
P3 = np.matrix([[0, -1, 2, -2], 
                [0, -1, 2, -1]], dtype=np.float64)

P3_prime1 = P3 + t1
P3_prime2 = P3 + t2
P3_prime3 = P3 + t3
P3_prime4 = P3 + t4

showPoints(P3_prime1, color="red")
#showPoints(P3_prime2, color="green")
#showPoints(P3_prime3, color="blue")
#showPoints(P3_prime4, color="yellow")


# Exercise 4.02.i
T_AB = transformation(50*math.pi/180, (7,5))

# Exercise 4.02.j
O_A = toHomogeneous(np.matrix([[0],[0]], dtype=np.float64))
#O_A = np.matrix([[0],[0], [1]], dtype=np.float64)
O_B = T_AB * O_A

"""
showPoints(O_B)
"""
# Exercise 4.02.k
# ???

# Exercise 4.02.l
P_A1 = toHomogeneous(np.matrix([[1],[0]], dtype=np.float64))
P_A2 = toHomogeneous(np.matrix([[0],[1]], dtype=np.float64))

P_B1 = T_AB * P_A1
P_B2 = T_AB * P_A2
"""
showPoints(P_B1, color='red')
showPoints(P_B2, color='red')
"""
# Exercise 4.02.m
T_BA = np.linalg.inv(T_AB)

# Exercise 4.02.n
P_A1 = T_BA * P_B1
P_A2 = T_BA * P_B2
"""
showPoints(P_A1, color='green')
showPoints(P_A2, color='green')
"""
# Exercise 4.02.n

# A transformation from A to B and from B to A, which means we get back to the original coordinate-system.

plt.show()
#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->
print ""
raw_input("Done. Press enter to terminate..")