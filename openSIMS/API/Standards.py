import copy
import numpy as np
import pandas as pd
import openSIMS as S
from . import Toolbox, Sample
from openSIMS.Methods import Functions
from scipy.optimize import minimize

def getStandards(simplex):

    datatype = S.settings(simplex.method)['type']
    if datatype == 'geochron':
        return GeochronStandards(simplex)
    elif datatype == 'stable':
        return StableStandards(simplex)
    else:
        raise ValueError('Unrecognised data type')

class Standards:

    def __init__(self,simplex):
        self.method = simplex.method
        self.standards = copy.copy(simplex.samples)
        for sname, sample in simplex.samples.items():
            if sample.group == 'sample' or sname in simplex.ignore:
                self.standards.drop(sname,inplace=True)

class GeochronStandards(Standards):

    def __init__(self,simplex):
        super().__init__(simplex)
    
    def calibrate(self):
        res = minimize(self.misfit,0.0,method='nelder-mead')
        b = res.x[0]
        x, y, A, B = self.fit(b)
        return {'A':A, 'B':B, 'b':b}
    
    def misfit(self,b):
        x, y, A, B = self.fit(b)
        SS = sum((A+B*x-y)**2)
        return SS

    def fit(self,b):
        x, y = self.pooled_calibration_data(b)
        A, B = Toolbox.linearfit(x,y)
        return x, y, A, B

    def pooled_calibration_data(self,b):
        x = np.array([])
        y = np.array([])
        for standard in self.standards.array:
            xn, yn = self.calibration_data(standard,b)
            dy = self.offset(standard)
            x = np.append(x,xn)
            y = np.append(y,yn-dy)
        return x, y

    def calibration_data(self,standard,b):
        settings = S.settings(self.method)
        function_name = settings['calibration_data']
        fun = getattr(Functions,function_name)
        return fun(standard,b)

    def offset(self,standard):
        method = S.settings(self.method)
        DP = method.get_DP(standard.group)
        L = method['lambda']
        y0t = np.log(DP)
        y01 = np.log(np.exp(L)-1)
        return y0t - y01
    
class StableStandards(Standards):

    def __init__(self,simplex):
        super().__init__(simplex)

    def calibrate(self):
        pass
    
    def misfit(self,b):
        pass
    
    def calibration_data(self,b):
        pass
