import copy
import numpy as np
from . import Refmats, Crunch
from scipy.optimize import minimize

class standards():

    def __init__(self,simplex):
        self.method = simplex.method
        self.samples = copy.copy(simplex.samples)
        for sname, sample in simplex.samples.items():
            if sample.group == 'sample' or sname in simplex.ignore:
                self.samples.drop(sname,inplace=True)

    def process(self):
        res = minimize(self.misfit,0.0,method='nelder-mead')
        b = res.x[0]
        x, y = self.calibration_data(b)
        A, B = Crunch.linearfit(x,y)
        return {'A':A, 'B':B, 'b':b}
    
    def misfit(self,b):
        x, y = self.calibration_data(b)
        A, B = Crunch.linearfit(x,y)
        SS = sum((A+B*x-y)**2)
        return SS

    def calibration_data(self,b):
        x = np.array([])
        y = np.array([])
        for standard in self.samples.array:
            xn, yn = standard.calibration_data_UPb(b)
            offset = Refmats.offset(self.method.name,standard.group)
            x = np.append(x,xn)
            y = np.append(y,yn-offset)
        return x, y
