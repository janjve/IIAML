#<--------------------------------------------------->
#<-- Simple Linear Regression on Contrived Dataset -->
#<--------------------------------------------------->
from math import sqrt
from matplotlib import pyplot as plt
import numpy as np

# plot actual and predicted outputs
def PlotOutputs(Dataset, PredictedOutput):
    X = [Row[0] for Row in Dataset]
    Y = [Row[1] for Row in Dataset]
    
    # plot actual
    plt.plot(X, Y, 'ko')
    plt.xlim(-1, 6)
    plt.ylim(-1, 6)
    plt.xlabel("Input")
    plt.ylabel("Output (actual/predicted)")
    # plot predicted
    plt.plot(X, PredictedOutput, 'r-o')
    
# Calculate root mean squared error
def rmse_metric(actual, predicted):
	sum_error = 0.0
	for i in range(len(actual)):
		prediction_error = predicted[i] - actual[i]
		sum_error += (prediction_error ** 2)
	mean_error = sum_error / float(len(actual))
	return sqrt(mean_error)

# Evaluate regression algorithm on training dataset
def evaluate_algorithm(dataset, algorithm):
	test_set = list()
	for row in dataset:
		row_copy = list(row)
		row_copy[-1] = None
		test_set.append(row_copy)
	predicted = algorithm(dataset, test_set)
	print(predicted)
	actual = [row[-1] for row in dataset]
	rmse = rmse_metric(actual, predicted)
	return rmse, predicted

# Calculate the mean value of a list of numbers
def mean(values):
	return sum(values) / float(len(values))

# Calculate covariance between x and y
def covariance(x, mean_x, y, mean_y):
	covar = 0.0
	for i in range(len(x)):
		covar += (x[i] - mean_x) * (y[i] - mean_y)
	return covar

# Calculate the variance of a list of numbers
def variance(values, mean):
	return sum([(x-mean)**2 for x in values])

# Calculate coefficients using statistical method
def coefficients(dataset):
	x = [row[0] for row in dataset]
	y = [row[1] for row in dataset]
	x_mean, y_mean = mean(x), mean(y)
	b1 = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
	b0 = y_mean - b1 * x_mean
	print b0, b1
	return [b0, b1]

# Calculate coefficients using least squares    
def coefficients_ls(train):
    A = np.matrix([[row[0], 1] for row in train])
    b = [[row[1]] for row in train]
    result = np.linalg.lstsq(A, b)[0]   
    return result[1][0], result[0][0]

# Simple linear regression algorithm
def simple_linear_regression(train, test):
	predictions = list()
	b0, b1 = coefficients(train)
	for row in test:
		yhat = b0 + b1 * row[0]
		predictions.append(yhat)
	return predictions

# Test simple linear regression on contrived dataset
dataset = [[1, 1], [2, 3], [3, 3], [4, 2], [5, 5]]

rmse, predicted = evaluate_algorithm(dataset, simple_linear_regression)
print('RMSE: %.3f' % (rmse))

# plot results
PlotOutputs(dataset, predicted)
plt.show()