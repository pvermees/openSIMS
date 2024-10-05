import numpy as np
import pandas as pd
import openSIMS as S
from . import Toolbox, Ellipse
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class Geochron:

    def get_csv(self,name):
        sample = self.samples.loc[name]
        settings = S.settings(self.method)
        ions = settings['ions']
        P = sample.cps(self.method,ions[0])
        POx = sample.cps(self.method,ions[1])
        D = sample.cps(self.method,ions[2])
        d = sample.cps(self.method,ions[3])
        return P, POx, D, d
    
    def offset(self,name):
        standard = self.samples.loc[name]
        settings = S.settings(self.method)
        DP = settings.get_DP(standard.group)
        L = settings['lambda']
        y0t = np.log(DP)
        y01 = np.log(np.exp(L)-1)
        return y0t - y01

    def get_labels(self):
        P, POx, D, d  = S.settings(self.method)['ions']
        channels = S.get('methods')[self.method]
        xlabel = 'ln(' + channels[POx] + '/' + channels[P] + ')'
        ylabel = 'ln(' + channels[D] + '/' + channels[P] + ')'
        return xlabel, ylabel

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
            x, y = self.get_xy(name,p['b'])
            Ellipse.confidence_ellipse(x,y,ax,alpha=0.25,facecolor=colour,
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
    
class Calibrator:

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
        for name in self.samples.keys():
            xn, yn = self.get_xy(name,b=b)
            dy = self.offset(name)
            x = np.append(x,xn)
            y = np.append(y,yn-dy)
        return x, y

    def get_xy(self,name,b=0.0):
        P, POx, D, d = self.get_csv(name)
        standard = self.samples.loc[name]
        settings = S.settings(self.method)
        y0 = settings.get_y0(standard.group)
        drift = np.exp(b*D['time']/60)
        x = np.log(POx['cps']) - np.log(P['cps'])
        y = np.log(drift*D['cps']-y0*d['cps']) - np.log(P['cps'])
        return x, y

class Processor:

    def process(self):
        out = dict()
        for name, sample in self.samples.items():
            x, y = self.get_xy(name,b=self.pars['b'])
            DP, dD = self.get_DPdD(name,x,y)
            out[name] = pd.DataFrame({'DP':DP,'dD':dD})
        return out

    def get_DPdD(self,name,x,y):
        P, POx, D, d = self.get_csv(name)
        yref = self.pars['A'] + self.pars['B']*D['time']
        DP = np.exp(y-yref)
        drift = np.exp(self.pars['b']*(d['time']-D['time'])/60)
        dD = drift*d['cps']/D['cps']
        return DP, dD

    def get_xy(self,name,b=0.0):
        settings = S.settings(self.method)
        P, POx, D, d = self.get_csv(name)
        Drift = np.exp(b*D['time']/60)
        drift = np.exp(b*d['time']/60)
        x = np.log(POx['cps']) - np.log(P['cps'])
        y = np.log(Drift*D['cps']) - np.log(P['cps'])
        return x, y
