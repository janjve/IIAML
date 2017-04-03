# Example of Simple Linear Regression on the Swedish Insurance Dataset
from random import seed
from random import randrange
from csv import reader
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

# plot actual and predicted outputs
def plot_outputs(dataset, predicted):
    x = [row[0] for row in dataset]
    y = [row[1] for row in dataset]
    
    # plot actual
    plt.plot(x, y, 'ko')
    plt.xlim(np.min(x) - 10, np.max(x) + 10)
    plt.ylim(np.min(y) - 10, np.max(y) + 10)
    plt.xlabel("Input")
    plt.ylabel("Output (actual/predicted)")
    # plot predicted
    plt.plot(x, predicted, 'r-o')
    
# Load a CSV file
def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset

# Convert string column to float
def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())

# Split a dataset into a train and test set
def train_test_split(dataset, split):
    train = list()
    train_size = split * len(dataset)
    dataset_copy = list(dataset)
    while len(train) < train_size:
        index = randrange(len(dataset_copy))
        train.append(dataset_copy.pop(index))
    return train, dataset_copy

# Calculate root mean squared error
def rmse_metric(actual, predicted):
    sum_error = 0.0
    for i in range(len(actual)):
        prediction_error = predicted[i] - actual[i]
        sum_error += (prediction_error ** 2)
    mean_error = sum_error / float(len(actual))
    return sqrt(mean_error)

# Evaluate an algorithm using a train/test split
def evaluate_algorithm(dataset, algorithm, split):
    #<------------------------------------------------------------------>
    #<---                     Your code here                         --->
    #<------------------------------------------------------------------>    
    
    train_set, test_set = train_test_split(dataset, split)
    prediction = algorithm(train_set, test_set)
    actual = [row[-1] for row in test_set]
    rmse = rmse_metric(actual, prediction)
    
    return (rmse, test_set, prediction)
    #<------------------------------------------------------------------>
    #<---                                                            --->
    #<------------------------------------------------------------------>

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

# Calculate coefficients using statistica method
def coefficients(dataset):
    x = [row[0] for row in dataset]
    y = [row[1] for row in dataset]
    x_mean, y_mean = mean(x), mean(y)
    b1 = covariance(x, x_mean, y, y_mean) / variance(x, x_mean)
    b0 = y_mean - b1 * x_mean
    return [b0, b1]

# Calculate coefficients using least squares    
def coefficients_ls(train):
    A = np.matrix([[row[0], 1] for row in train])
    b = [[row[1]] for row in train]
    result = np.linalg.lstsq(A, b)[0]   
    return result[1][0], result[0][0]

# Simple linear regression algorithm
def linear_regression(train, test):
    predictions = list()
    # approximate coefficients using statistical method
    b0, b1 = coefficients(train)
    # approximate coefficients using least squares
    #b0, b1 = coefficients_ls(train)
    for row in test:
        yhat = b0 + b1 * row[0]
        predictions.append(yhat)
    return predictions


# Simple linear regression on insurance dataset
seed(1)
# load and prepare data
filename = 'insurance.csv'
dataset = load_csv(filename)
for i in range(len(dataset[0])):
    str_column_to_float(dataset, i)
    
# evaluate algorithm
split = 0.6

#<------------------------------------------------------------------>
#<---                     Your code here                         --->
#<------------------------------------------------------------------>
rmse, test, predicted, percentile = (100000., [], [], -1)

for percent in range(5, 95, 1):
    split = percent / 100.
    (r, t, p) = evaluate_algorithm(dataset, linear_regression, split)
    print str(percent) + " % split RMSE: " + str(r)
    if r < rmse:
        rmse, test, predicted = (r, t, p)
        percentile = percent

print "optimal RMSE (" + str(percentile) + "): ", str(rmse)
#<------------------------------------------------------------------>
#<---                                                            --->
#<------------------------------------------------------------------>

# plot results
plot_outputs(test, predicted)
plt.show()