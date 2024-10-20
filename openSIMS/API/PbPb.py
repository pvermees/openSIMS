import numpy as np
import scipy as sp
import pandas as pd
import openSIMS as S
from . import Toolbox, Ellipse
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class PbPb:

    def get_cps(self,name):
        sample = self.samples.loc[name]
        settings = S.settings(self.method)
        ions = settings['ions']
        Pb7 = sample.cps(self.method,ions[0])
        Pb6 = sample.cps(self.method,ions[1])
        Pb4 = sample.cps(self.method,ions[2])
        return Pb7, Pb6, Pb4
    
    def get_labels(self):
        Pb7, Pb6, Pb4  = S.settings(self.method)['ions']
        channels = S.get('methods')[self.method]
        xlabel = channels[Pb7] + '/' + channels[Pb6]
        ylabel = channels[Pb4] + '/' + channels[Pb6]
        return xlabel, ylabel

    def process(self):
        self.results = Results(self.method)
        for name, sample in self.samples.items():
            pass

class Calibrator:

    def calibrate(self):
        res = minimize(self.misfit,[0.0,0.0],method='nelder-mead')
        a = res.x[0]
        b = res.x[1]
        self.pars = {'a':a,'b':b}
        
    def misfit(self,ab=[0.0,0.0]):
        a, b = ab
        SS = 0.0
        for name in self.samples.keys():
            standard = self.samples.loc[name]
            settings = S.settings(self.method)
            A = settings.get_Pb76(standard.group)
            B = settings.get_Pb74_0(standard.group)
            SS += self.get_SS(name,A,B,a=a,b=b)
        return SS

    def get_SS(self,name,A,B,a=0.0,b=0.0):
        Pb7, Pb6, Pb4 = self.get_cps(name)
        m7 = Pb7['cps']
        tt7 = Pb7['time']
        m6 = Pb6['cps']
        tt6 = Pb6['time']
        m4 = Pb4['cps']
        tt4 = Pb4['time']
        num4 = B*m7*np.exp(b*tt7+2*a) + \
            (A**2*m4*np.exp(b*tt4+4*a)-A*B*np.exp(3*a)*m6)*np.exp(2*b*tt7) + \
            m4*np.exp(b*tt4+2*a)
        den4 = (A**2*np.exp(2*b*tt4+2*a)+B**2)*np.exp(2*b*tt7) + np.exp(2*b*tt4)
        t4 = num4/den4
        num6 = (-A*m7*np.exp(b*tt7+2*b*tt4+a)) + \
            (A*B*m4*np.exp(b*tt4+a)-B**2*m6)*np.exp(2*b*tt7) - \
            m6*np.exp(2*b*tt4)
        den6 = (A**2*np.exp(2*b*tt4+2*a)+B**2)*np.exp(2*b*tt7) + np.exp(2*b*tt4)
        t6 = -num6/den6
        SS = (A*t6*np.exp(b*tt7+a) + B*t4*np.exp(b*tt7-2*a)-m7)**2 + \
            (t4*np.exp(b*tt4-2*a)-m4)**2+(t6-m6)**2
        return sum(SS)

    def plot(self,fig=None,ax=None):
        p = self.pars
        if fig is None or ax is None:
            fig, ax = plt.subplots()
        lines = dict()
        np.random.seed(1)
        for name, sample in self.samples.items():
            group = sample.group
            if group in lines.keys():
                colour = lines[group]['colour']
            else:
                colour = np.random.rand(3,)
                lines[group] = dict()
                lines[group]['colour'] = colour
        xlabel, ylabel = self.get_labels()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        for group, val in lines.items():
            if group == 'sample':
                pass
            else:
                pass
        fig.tight_layout()
        return fig, ax

class Processor:
    
    def plot(self,fig=None,ax=None):
        p = self.pars
        if fig is None or ax is None:
            fig, ax = plt.subplots()
        lines = dict()
        np.random.seed(1)
        results = self.results.average()
        for sname, sample in self.samples.items():
            pass
        xlabel, ylabel = self.get_labels()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.tight_layout()
        return fig, ax
    
class Results(dict):

    def __init__(self,method):
        super().__init__()

    def average(self):
        pass

class Result(pd.DataFrame):

    def ages(self):
        pass
