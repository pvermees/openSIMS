import numpy as np

def linearfit(x,y):
    D = np.vstack([x, np.ones(len(x))]).T
    y = y[:, np.newaxis]
    res = np.dot((np.dot(np.linalg.inv(np.dot(D.T,D)),D.T)),y)
    slope = res[0][0]
    intercept = res[1][0]
    return intercept, slope
    








