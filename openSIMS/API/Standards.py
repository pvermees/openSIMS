import copy
import math
import numpy as np
import pandas as pd
import openSIMS as S
import matplotlib.pyplot as plt
from . import Toolbox, Sample, Ellipse
from scipy.optimize import minimize
from abc import ABC, abstractmethod

def getStandards(simplex,method=None):
    if method is None:
        method = list(simplex.methods.keys())[0]
    datatype = S.settings(method)['type']
    if datatype == 'geochron':
        return GeochronStandards(simplex,method)
    elif datatype == 'stable':
        return StableStandards(simplex,method)
    else:
        raise ValueError('Unrecognised data type')

class Standards(ABC):

    def __init__(self,simplex,method):
        self.pars = simplex.get_pars(method)
        self.method = method
        self.standards = copy.copy(simplex.samples)
        for sname, sample in simplex.samples.items():
            if sample.group == 'sample' or sname in simplex.ignore:
                self.standards.drop(sname,inplace=True)

    @abstractmethod
    def calibrate(self):
        pass

    @abstractmethod
    def plot(self):
        pass

class GeochronStandards(Standards):

    def __init__(self,simplex,method):
        super().__init__(simplex,method)
    
    def calibrate(self):
        res = minimize(self.misfit,0.0,method='nelder-mead')
        b = res.x[0]
        x, y, A, B = self.fit(b)
        return {'A':A, 'B':B, 'b':b}
   
    def misfit(self,b=0.0):
        x, y, A, B = self.fit(b)
        SS = sum((A+B*x-y)**2)
        return SS

    def fit(self,b=0.0):
        x, y = self.pooled_calibration_data(b=b)
        A, B = Toolbox.linearfit(x,y)
        return x, y, A, B

    def pooled_calibration_data(self,b=0.0):
        x = np.array([])
        y = np.array([])
        settings = S.settings(self.method)
        for name in self.standards.keys():
            xn, yn = self.raw_calibration_data(name,b=b)
            dy = self.offset(name)
            x = np.append(x,xn)
            y = np.append(y,yn-dy)
        return x, y

    def raw_calibration_data(self,name,b=0.0):
        standard = self.standards.loc[name]
        settings = S.settings(self.method)
        ions = settings['ions']
        P = standard.cps(self.method,ions[0])
        POx = standard.cps(self.method,ions[1])
        D = standard.cps(self.method,ions[2])
        d = standard.cps(self.method,ions[3])
        drift = np.exp(b*D['time']/60)
        y0 = settings.get_y0(standard.group)
        x = np.log(POx['cps']) - np.log(P['cps'])
        y = np.log(drift*D['cps']-y0*d['cps']) - np.log(P['cps'])
        return x, y

    def offset(self,name):
        standard = self.standards.loc[name]
        settings = S.settings(self.method)
        DP = settings.get_DP(standard.group)
        L = settings['lambda']
        y0t = np.log(DP)
        y01 = np.log(np.exp(L)-1)
        return y0t - y01

    def plot(self,fig=None,ax=None):
        p = self.pars
        if fig is None or ax is None:
            fig, ax = plt.subplots()
        lines = dict()
        np.random.seed(0)
        for name, standard in self.standards.items():
            group = standard.group
            if group in lines.keys():
                colour = lines[group]['colour']
            else:
                colour = np.random.rand(3,)
                lines[group] = dict()
                lines[group]['colour'] = colour
                lines[group]['offset'] = self.offset(name)
            x, y = self.raw_calibration_data(name,p['b'])
            Ellipse.confidence_ellipse(x,y,ax,alpha=0.25,facecolor=colour,
                                       edgecolor='black',zorder=0)
            ax.scatter(np.mean(x),np.mean(y),s=3,c='black')
        xmin = ax.get_xlim()[0]
        xlabel, ylabel = self.get_labels()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        for group, val in lines.items():
            ymin = p['A'] + val['offset'] + p['B'] * xmin
            ax.axline((xmin,ymin),slope=p['B'],color=val['colour'])
        return fig, ax

    def get_labels(self):
        P, POx, D, d  = S.settings(self.method)['ions']
        channels = S.get('methods')[self.method]
        xlabel = 'ln(' + channels[POx] + '/' + channels[P] + ')'
        ylabel = 'ln(' + channels[D] + '/' + channels[P] + ')'
        return xlabel, ylabel
        
class StableStandards(Standards):

    def __init__(self,simplex,method):
        super().__init__(simplex,method)

    def calibrate(self):
        logratios = self.pooled_calibration_data()
        return logratios.mean(axis=0)
            
    def pooled_calibration_data(self):
        df_list = []
        for standard in self.standards.array:
            logratios = self.raw_logratios(standard)
            offset = self.offset(standard)
            df = logratios.apply(lambda raw: raw - offset.values, axis=1)
            df_list.append(df)
        return pd.concat(df_list)

    def get_num_den(self):
        settings = S.settings(self.method)
        num = settings['deltaref']['num']
        den = settings['deltaref']['den']
        return num, den

    def get_ratios(self):
        num, den = self.get_num_den()
        ratios = [f"{n}/{d}" for n, d in zip(num, den)]
        return num, den, ratios

    def raw_logratios(self,standard):
        num, den, ratios = self.get_ratios()
        raw_cps = self.raw_calibration_data(standard)
        out = np.log(raw_cps[num]) - np.log(raw_cps[den]).values
        return out.set_axis(ratios,axis=1)

    def raw_calibration_data(self,standard):
        settings = S.settings(self.method)
        ions = settings['ions']
        out = pd.DataFrame()
        for ion in ions:
            out[ion] = standard.cps(self.method,ion)['cps']
        return out

    def offset(self,standard):
        num, den, ratios = self.get_ratios()
        settings = S.settings(self.method)
        delta = settings['refmats'][ratios].loc[standard.group]
        return np.log(delta+1)
        
    def plot(self):
        num_panels = len(self.pars)
        ratio_names = self.pars.index.to_list()
        nr = math.ceil(math.sqrt(num_panels))
        nc = math.ceil(num_panels/nr)
        fig, ax = plt.subplots(nrows=nr,ncols=nc)
        lines = dict()
        np.random.seed(0)
        for sname, standard in self.standards.items():
            group = standard.group
            if group in lines.keys():
                colour = lines[group]['colour']
            else:
                colour = np.random.rand(3,)
                lines[group] = dict()
                lines[group]['colour'] = colour
                lines[group]['offset'] = self.offset(standard)
            raw_logratios = self.raw_logratios(standard)
            nsweeps = raw_logratios.shape[0]
            logratio_means = raw_logratios.mean(axis=0)
            logratio_stderr = raw_logratios.std(axis=0)/math.sqrt(nsweeps)
            for i, ratio_name in enumerate(ratio_names):
                y_mean = logratio_means.iloc[i]
                y_min = y_mean - logratio_stderr.iloc[i]
                y_max = y_mean + logratio_stderr.iloc[i]
                ax.ravel()[i].scatter(sname,y_mean,
                                      s=5,color='black',zorder=2)
                ax.ravel()[i].plot([sname,sname],[y_min,y_max],
                                   '-',color=colour,zorder=1)
        for i, ratio_name in enumerate(ratio_names):
            title = 'ln(' + ratio_name + ')'
            ax.ravel()[i].set_title(title)
        for group, val in lines.items():
            y = self.pars + val['offset']
            for i, ratio_name in enumerate(ratio_names):
                ax.ravel()[i].axline((0.0,y[ratio_name]),slope=0.0,
                                     color=val['colour'],zorder=0)
        for empty_axis in range(len(ratio_names),nr*nc):
            fig.delaxes(ax.flatten()[empty_axis])
        fig.tight_layout()
        return fig, ax
