import copy
import numpy as np
import pandas as pd
import openSIMS as S
from . import Toolbox, Sample
from scipy.optimize import minimize
from abc import ABC, abstractmethod

def getStandards(simplex):

    datatype = S.settings(simplex.method)['type']
    if datatype == 'geochron':
        return GeochronStandards(simplex)
    elif datatype == 'stable':
        return StableStandards(simplex)
    else:
        raise ValueError('Unrecognised data type')

class Standards(ABC):

    def __init__(self,simplex):
        self.method = simplex.method
        self.standards = copy.copy(simplex.samples)
        for sname, sample in simplex.samples.items():
            if sample.group == 'sample' or sname in simplex.ignore:
                self.standards.drop(sname,inplace=True)

    @abstractmethod
    def calibrate(self):
        pass

    @abstractmethod
    def misfit(self,b):
        pass
    
    @abstractmethod
    def pooled_calibration_data(self,b):
        pass

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
        settings = S.settings(self.method)
        for standard in self.standards.array:
            xn, yn = self.calibration_data(settings,standard,b)
            dy = self.offset(settings,standard)
            x = np.append(x,xn)
            y = np.append(y,yn-dy)
        return x, y

    @staticmethod
    def calibration_data(settings,standard,b):
        ions = settings['ions']
        P = standard.cps(ions[0])
        POx = standard.cps(ions[1])
        D = standard.cps(ions[2])
        d = standard.cps(ions[3])
        drift = np.exp(b*D['time']/60)
        y0 = settings.get_y0(standard.group)
        x = np.log(POx['cps']) - np.log(P['cps'])
        y = np.log(drift*D['cps']-y0*d['cps']) - np.log(P['cps'])
        return x, y

    @staticmethod
    def offset(settings,standard):
        DP = settings.get_DP(standard.group)
        L = settings['lambda']
        y0t = np.log(DP)
        y01 = np.log(np.exp(L)-1)
        return y0t - y01
    
class StableStandards(Standards):

    def __init__(self,simplex):
        super().__init__(simplex)

    def calibrate(self):
        ratios = self.pooled_calibration_data()
            
    def misfit(self,b):
        pass
    
    def pooled_calibration_data(self):
        settings = S.settings(self.method)
        num = settings['deltaref']['num']
        den = settings['deltaref']['den']
        ratios = np.array([])
        for standard in self.standards.array:
            pass

    def offset(self,standard):
        method = S.settings(self.method)
