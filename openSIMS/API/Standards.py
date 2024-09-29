import copy
import numpy as np
import pandas as pd
import openSIMS as S
import matplotlib.pyplot as plt
from . import Toolbox, Sample, Ellipse
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
        self.pars = simplex.pars
        self.method = simplex.method
        self.channels = simplex.channels
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

    @abstractmethod
    def plot(self):
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
            xn, yn = self.raw_calibration_data(standard,b)
            dy = self.offset(standard)
            x = np.append(x,xn)
            y = np.append(y,yn-dy)
        return x, y

    def raw_calibration_data(self,standard,b):
        settings = S.settings(self.method)
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

    def offset(self,standard):
        settings = S.settings(self.method)
        DP = settings.get_DP(standard.group)
        L = settings['lambda']
        y0t = np.log(DP)
        y01 = np.log(np.exp(L)-1)
        return y0t - y01

    def plot(self,show=True,num=None):
        p = self.pars
        fig, ax = plt.subplots()
        lines = dict()
        np.random.seed(0)
        for sname, standard in self.standards.items():
            group = standard.group
            if group in lines.keys():
                colour = lines[group]['colour']
            else:
                lines[group] = dict()
                lines[group]['colour'] = np.random.rand(3,)
                lines[group]['offset'] = self.offset(standard)
            x, y = self.raw_calibration_data(standard,p['b'])
            Ellipse.confidence_ellipse(x,y,ax,
                                       alpha=0.25,
                                       facecolor=lines[group]['colour'],
                                       edgecolor='black',
                                       zorder=0)
            ax.scatter(np.mean(x),np.mean(y),s=3,c='black')
        xmin = ax.get_xlim()[0]
        for group, val in lines.items():
            ymin = p['A'] + val['offset'] + p['B'] * xmin
            ax.axline((xmin,ymin),slope=p['B'],color=val['colour'])
        if show:
            plt.show()
        return fig, ax

class StableStandards(Standards):

    def __init__(self,simplex):
        super().__init__(simplex)

    def calibrate(self):
        logratios = self.pooled_calibration_data()
        return logratios.mean
            
    def misfit(self,b=0):
        pass
    
    def pooled_calibration_data(self,b=0):
        settings = S.settings(self.method)
        num = settings['deltaref']['num']
        den = settings['deltaref']['den']
        ratios = [f"{n}/{d}" for n, d in zip(num, den)]
        df_list = []
        for standard in self.standards.array:
            raw_cps = self.raw_calibration_data(settings,standard,b=b)
            logratios = np.log(raw_cps[num]) - np.log(raw_cps[den]).values
            offset = self.offset(settings,standard,ratios,b=b)
            logratios.apply(lambda raw: raw - offset.values, axis=1)
            df_list.append(logratios)
        out = pd.concat(df_list)
        out.set_axis(ratios,axis=1)
        return out

    @staticmethod
    def raw_calibration_data(settings,standard,b=0):
        ions = settings['ions']
        out = pd.DataFrame()
        for ion in ions:
            out[ion] = standard.cps(ion)['cps']
        return out

    @staticmethod
    def offset(settings,standard,ratios,b=0):
        ratios = settings['refmats'][ratios].loc[standard.group]
        ratios_deltaref = settings['deltaref']['ratio']
        return np.log(ratios) - np.log(ratios_deltaref)
        
    def plot(self,show=True,num=None):
        pass
