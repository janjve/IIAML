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
plt.show()

# Create a column of ones.
ones = np.ones((m, 1))

#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->



#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->
