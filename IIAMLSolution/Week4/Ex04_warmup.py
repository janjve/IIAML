#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex04_warmup.py                                           -->
#<!-- Description: Script to create matrices using Numpy and to calculate   -->
#<!--            : some mathematical operations between two matrices        -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kopenhagen S.   -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 03/12/2016                                               -->
#<!-- Change     : 03/12/2016 - Development of this exercise                -->
#<!-- Review     : 17/02/2017 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2017021701 $"

########################################################################
import numpy as np

########################################################################

#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->

# Exercise 4.01.a
A = np.array([[1.0000, 0.0500, 0.3333, 0.2500],
              [0.5000, 0.3333, 0.2500, 0.2000],
              [0.3333, 0.2500, 0.2000, 0.1667],
              [0.2500, 0.2000, 0.1667, 0.1429]], 
             dtype = np.float64)

B = np.array([[-16., 15., -14., 13.],
              [-12., 14., -10., 9.],
              [-8.,   7., -6.,  5.],
              [-4.,   3., -2.,  1.]], 
             dtype = np.float64)

C = np.array([[1,    1./1, 1./2, 1./3],
              [1./2, 1./3, 1./4, 1./5],
              [1./3, 1./5, 1./6, 1./7],
              [1./4, 1./7, 1./8, 1./9]], 
             dtype = np.float64)
"""
print A
print B
print C
"""
# Exercise 4.01.b

print np.array(A - B, dtype = np.float64)
print np.array(A - B, dtype = np.float16)

# Exercise 4.01.c
# This does not show anything.
"""
print np.dot(A, C)
print np.dot(B, C)
"""
# Assumed Real question
"""
print np.dot(A, C)
print np.dot(C, A)
"""
# Exercise 4.01.d
"""
print A * C
print B * C
"""
# * = indexwise multiplication, np.dot = matrix multiplication

# Exercise 4.01.e
# The inverse of a square matrix A is the matrix A^-1, such that A(A^-1) = I

# If the determinant is 0 there is no inverse matrix.
"""
print np.linalg.det(A)
print np.linalg.det(B)
print np.linalg.det(C)
"""
# C does not have an inverse matrix.

# Exercise 4.01.f
"""
print np.linalg.inv(A)
print np.linalg.inv(B)
#print np.linalg.inv(C) # Will fail
"""
D = np.array([[2.,    4.,  5./2],
              [-3./4, 2.,  0.25],
              [0.25,  0.5, 2.]], dtype=np.float64)

E = np.array([[1.,   -0.5, 3./4],
              [3./2,  0.5, -2.],
              [0.25,  1.,  0.5]], dtype=np.float64)

# Exercise 4.01.g
"""
print np.linalg.inv(D).dot(np.linalg.inv(E))    # 1
print np.linalg.inv(D.dot(E))                   # 2
print np.linalg.inv(E.dot(D))                   # 3
"""
# #1 and #3 gives the same result, because of the rule
# (ABC)^-1 = C^-1 * B^-1 * A^-1. If we let C be the identity matrix I, we get:
# (ABI)^-1 = I^-1 * B^-1 * A^-1 <=> (AB)^-1 = B^-1 * A^-1, which means that #1 = #3.

# exercise 4.01.h
"""
print np.linalg.inv(D).T                        # 4
print np.linalg.inv(D.T)                        # 5
"""
# #4 and #5 yields the same result, because of the rule:
# (A^T)^-1 = (A^-1)^T, which is exactly what we just showed.

#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->

print ""
raw_input("Done. Press enter to terminate..")