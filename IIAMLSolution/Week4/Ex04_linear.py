#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex04_linear.py                                           -->
#<!-- Description: Script to solve linear equation systems                  -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kopenhagen S.   -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 09/12/2016                                               -->
#<!-- Change     : 09/12/2016 - Development of this exercise                -->
#<!-- Review     : 17/02/2017 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2017021701 $"

########################################################################
import matplotlib.pyplot as plt
import numpy as np

########################################################################

# This function creates a Matplotlib window and shows four histograms.
def showData(data, marker="x", color="black", title="World Population in Billions"):
    plt.title(title)
    plt.xlim([1950, 2005])
    plt.xlabel("Year")
    plt.ylabel("Population in Billions")
    plt.scatter(data[:, 0], data[:, 1], marker=marker, color=color)
    
#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->

# Exercise 4.03 (a) and (b) [WarmUp]
A = np.matrix([[2, 3, 4],
               [1, 4, 1],
               [4, 5, 2]], dtype=np.float64)
b = np.array([[2], [-2], [3]], dtype=np.float64)
x = np.linalg.solve(A,b)                    # Built-in
x1 = (np.linalg.inv(A.T * A) * A.T) * b     # Least squared - Pseudoinverse function
"""
print x
print x1
"""
# The results are the same

#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->

# Open the data set and create X, y and m variables.
# X: years.
# y: population in bilions.
data = np.loadtxt("data.txt", delimiter=",")
X = np.array([data[:, 0]]).T
y = np.array([data[:, 1]]).T
m = len(y)

# Plot the training dataset.
plt.figure("Input Data")
showData(data)


# Create a column of ones.
ones = np.ones((m, 1))

#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->

Y = np.c_[y,ones]
res = np.linalg.lstsq(Y, X)[0]
#print res
a = res[0][0]
b = res[1][0]

p1y = 1955.
p2y = 2000.
p1x = (p1y - b) / a
p2x = (p2y - b) / a

plt.plot ([ p1y , p2y], [p1x , p2x ], 'r-') # p1 and p2 are the extreme points of the line.


X1 = np.array([[1990, 1], [1995, 1], [2000, 1], [2050, 1]])
Y1 = (X1 - b) / a
print Y1[:,0]

#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->
plt.show()
print ""
raw_input("Done. Press enter to terminate..")