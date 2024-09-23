import openSIMS as S
import numpy as np
from . import Refmats

def misfit(b,standards):
    x, y = getxy(b,standards)
    A, B = linearfit(x,y)
    SS = sum((A+B*x-y)**2)
    return SS

def getxy(b,standards):
    x = np.array([])
    y = np.array([])
    for sname, standard in standards.items():
        U, UO, Pb4, Pb6, t = standard.misfit_data_UPb()
        offset, a0 = Refmats.offset('U-Pb',standard.group)
        drift = np.exp(b*t/60)
        x = np.append(x, np.log(UO)-np.log(U))
        y = np.append(y, np.log(drift*Pb6-a0*Pb4)-np.log(U)-offset)
    return x, y

def linearfit(x,y):
    D = np.vstack([x, np.ones(len(x))]).T
    y = y[:, np.newaxis]
    res = np.dot((np.dot(np.linalg.inv(np.dot(D.T,D)),D.T)),y)
    slope = res[0][0]
    intercept = res[1][0]
    return intercept, slope
    








