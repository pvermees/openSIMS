import copy
import numpy as np
import pandas as pd
import openSIMS as S
from . import Toolbox, Sample
from scipy.optimize import minimize

class Standards():

    def __init__(self,simplex):
        self.method = simplex.method
        self.standards = pd.Series()
        for sname, sample in simplex.samples.items():
            if sample.group != 'sample' and sname not in simplex.ignore:
                self.standards[sname] = Standard(sample)

    def process(self):
        res = minimize(self.misfit,0.0,method='nelder-mead')
        b = res.x[0]
        x, y = self.calibration_data(b)
        A, B = Toolbox.linearfit(x,y)
        return {'A':A, 'B':B, 'b':b}
    
    def misfit(self,b):
        x, y = self.calibration_data(b)
        A, B = Toolbox.linearfit(x,y)
        SS = sum((A+B*x-y)**2)
        return SS

    def calibration_data(self,b):
        x = np.array([])
        y = np.array([])
        for standard in self.standards.array:
            xn, yn = standard.calibration_data_UPb(b)
            offset = standard.offset()
            x = np.append(x,xn)
            y = np.append(y,yn-offset)
        return x, y

class Standard(Sample.Sample):

    def __init__(self,sample):
        self.__dict__ = sample.__dict__.copy()

    def offset(self):
        method = S.settings(self.method)
        DP = method.get_DP(self.group)
        L = method['lambda']
        y0t = np.log(DP)
        y01 = np.log(np.exp(L)-1)
        return y0t - y01
    
