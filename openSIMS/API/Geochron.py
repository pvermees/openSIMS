import numpy as np
import scipy as sp
import pandas as pd
import openSIMS as S
from . import Toolbox, Ellipse
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class Geochron:

    def get_cps(self,name):
        sample = self.samples.loc[name]
        settings = S.settings(self.method)
        ions = settings['ions']
        P = sample.cps(self.method,ions[0])
        POx = sample.cps(self.method,ions[1])
        D = sample.cps(self.method,ions[2])
        d = sample.cps(self.method,ions[3])
        return P, POx, D, d
    
    def get_labels(self):
        P, POx, D, d  = S.settings(self.method)['ions']
        channels = S.get('methods')[self.method]
        xlabel = 'ln(' + channels[POx] + '/' + channels[P] + ')'
        ylabel = 'ln(' + channels[D] + '/' + channels[P] + ')'
        return xlabel, ylabel

    def get_xy(self,name,b=0.0,y0=0.0):
        settings = S.settings(self.method)
        P, POx, D, d = self.get_cps(name)
        drift = np.exp(b*D['time']/60)
        x = np.log(POx['cps']) - np.log(P['cps'])
        y = np.log(drift*D['cps']-y0*d['cps']) - np.log(P['cps'])
        return x, y

    def get_tPDd(self,name,x,y):
        P, POx, D, d = self.get_cps(name)
        y_1Ma = self.pars['A'] + self.pars['B']*x
        DP_1Ma = S.settings(self.method).get_DP_1Ma()
        DP = np.exp(y-y_1Ma) * DP_1Ma
        drift = np.exp(self.pars['b']*(d['time']-D['time'])/60)
        tout = D['time']
        Dout = D['cps']
        Pout = Dout/DP
        dout = drift*d['cps']
        return pd.DataFrame({'t':tout,'P':Pout,'D':Dout,'d':dout})

    def process(self):
        self.results = Results(self.method)
        for name, sample in self.samples.items():
            self.results[name] = self.get_result(name,sample)

    def get_result(self,name,sample):
        s0 = dict()
        for ion, channel in S.get('methods')[self.method].items():
            tt = sample.total_time(self.method,[channel])
            breakpoint()
            s0[ion] = 3.688879/1.96/float(tt)
        x, y = self.get_xy(name,b=self.pars['b'])
        df = self.get_tPDd(name,x,y)
        return Result(df,s0)

class Calibrator:

    def calibrate(self):
        res = minimize(self.misfit,0.0,method='nelder-mead')
        b = res.x[0]
        x, y, A, B = self.fit(b)
        self.pars = {'A':A, 'B':B, 'b':b}
   
    def misfit(self,b=0.0):
        x, y, A, B = self.fit(b)
        SS = sum((A+B*x-y)**2)
        return SS

    def fit(self,b=0.0):
        x, y = self.pooled_calibration_data(b=b)
        A, B = Toolbox.linearfit(x,y)
        return x, y, A, B

    def offset(self,name):
        standard = self.samples.loc[name]
        settings = S.settings(self.method)
        DP = settings.get_DP(standard.group)
        DP_1Ma = settings.get_DP_1Ma()
        return np.log(DP) - np.log(DP_1Ma)

    def pooled_calibration_data(self,b=0.0):
        x = np.array([])
        y = np.array([])
        for name in self.samples.keys():
            xn, yn = self.get_xy_calibration(name,b=b)
            dy = self.offset(name)
            x = np.append(x,xn)
            y = np.append(y,yn-dy)
        return x, y

    def get_xy_calibration(self,name,b=0.0):
        standard = self.samples.loc[name]
        settings = S.settings(self.method)
        y0 = settings.get_y0(standard.group)
        return self.get_xy(name,b=b,y0=y0)

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
                if group != 'sample':
                    lines[group]['offset'] = self.offset(name)
            result = self.get_result(name,sample)
            mx, sx, my, sy, rho = result.average()
            Ellipse.result2ellipse(mx,sx,my,sy,rho,ax,
                                   alpha=0.25,facecolor=colour,
                                   edgecolor='black',zorder=0)
            ax.scatter(np.mean(x),np.mean(y),s=3,c='black')
        xmin = ax.get_xlim()[0]
        xlabel, ylabel = self.get_labels()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        for group, val in lines.items():
            if group == 'sample':
                pass
            else:
                ymin = p['A'] + val['offset'] + p['B'] * xmin
                ax.axline((xmin,ymin),slope=p['B'],color=val['colour'])
        fig.tight_layout()
        return fig, ax

class Processor:
    
    def plot(self,fig=None,ax=None):
        p = self.pars
        if fig is None or ax is None:
            fig, ax = plt.subplots()
        for result in self.results():
            mx, sx, my, sy, rho = result.average()
            Ellipse.result2ellipse(mx,sx,my,sy,rho,ax,
                                   alpha=0.25,facecolor='blue',
                                   edgecolor='black',zorder=0)
        xmin = ax.get_xlim()[0]
        xlabel, ylabel = self.get_labels()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.tight_layout()
        return fig, ax
    
class Results(dict):

    def __init__(self,method):
        super().__init__()
        self.labels = S.settings(method).get_labels()

    def average(self):
        lst = []
        for name, result in self.items():
            lst.append(result.average())
        out = pd.DataFrame(lst)
        labels = ['']*5
        labels[0] = self.labels['P'] + '/' + self.labels['D']
        labels[1] = 's[' + labels[0] + ']'
        labels[2] = self.labels['d'] + '/' + self.labels['D']
        labels[3] = 's[' + labels[2] + ']'
        labels[4] = 'rho[' + labels[0] + ',' + labels[2] + ']'
        out.columns = labels
        out.index = list(self.keys())
        return out

class Result():

    def __init__(self,tPb764,s0):
        self.df = tPb764
        self.s0 = s0

    def ages(self):
        pass

    def raw_PDdD(self):
        PD = self['P']/self['D']
        dD = self['d']/self['D']
        return PD, dD

    def average(self):
        pass
