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
        xlabel = channels[Pb4] + '/' + channels[Pb6]
        ylabel = channels[Pb7] + '/' + channels[Pb6]
        return xlabel, ylabel

    def get_tPb764(self,name):
        cps7, cps6, cps4 = self.get_cps(name)
        a = self.pars['a']
        b = self.pars['b']
        tt7 = cps7['time']/60
        Pb4 = cps4['cps']/np.exp(3*a+b*tt7)
        Pb6 = cps6['cps']/np.exp(a+b*tt7)
        return pd.DataFrame({'t':tt7,'Pb7':cps7['cps'],'Pb6':Pb6,'Pb4':Pb4})

    def get_xy(self,name):
        df = self.get_tPb764(name)
        x = df['Pb4']/df['Pb6']
        y = df['Pb7']/df['Pb6']
        return x, y

    def process(self):
        self.results = Results()
        for name, sample in self.samples.items():
            df = self.get_tPb764(name)
            self.results[name] = Result(df)

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
        tt7 = Pb7['time']/60
        m6 = Pb6['cps']
        tt6 = Pb6['time']/60
        m4 = Pb4['cps']
        tt4 = Pb4['time']/60
        num4 = t4 = m4*(np.exp(2*b*tt6+4*a)+A**2*np.exp(2*a))*np.exp(b*tt7) + \
            B*m7*np.exp(2*b*tt6+a) - A*B*m6*np.exp(b*tt6)
        den4 = (np.exp(2*b*tt6+7*a)+A**2*np.exp(5*a))*np.exp(2*b*tt7) + \
            B**2*np.exp(2*b*tt6+a)
        t4 = num4/den4
        num6 = (-A*B*m4*np.exp(b*tt7+2*a)) + \
            (m6*np.exp(b*tt6+6*a)+A*np.exp(5*a)*m7)*np.exp(2*b*tt7) + \
            B**2*m6*np.exp(b*tt6)
        den6 = (np.exp(2*b*tt6+7*a)+A**2*np.exp(5*a))*np.exp(2*b*tt7) + \
            B**2*np.exp(2*b*tt6+a)
        t6 = num6/den6
        SS = (t4*np.exp(b*tt7+3*a)-m4)**2 + \
            (t6*np.exp(b*tt6+a)-m6)**2 + (A*t6+B*t4-m7)**2
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
                settings = S.settings(self.method)
                colour = np.random.rand(3,)
                lines[group] = dict()
                lines[group]['colour'] = colour
                lines[group]['A'] = settings.get_Pb76(sample.group)
                lines[group]['B'] = settings.get_Pb74_0(sample.group)
            x,y = self.get_xy(name)
            Ellipse.xy2ellipse(x,y,ax,alpha=0.25,facecolor=colour,
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
                pass
                ymin = lines[group]['A'] + lines[group]['B'] * xmin
                ax.axline((xmin,ymin),slope=lines[group]['B'],color=val['colour'])
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
            x, y = self.get_xy(sname)
            Ellipse.xy2ellipse(x,y,ax,alpha=0.25,facecolor='blue',
                               edgecolor='black',zorder=0)
            ax.scatter(np.mean(x),np.mean(y),s=3,c='black')
        xlabel, ylabel = self.get_labels()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.tight_layout()
        return fig, ax
    
class Results(dict):

    def __init__(self):
        super().__init__()

    def average(self):
        lst = []
        for name, result in self.items():
            lst.append(result.avg_Pb764())
        out = pd.DataFrame(lst)
        labels = ['']*5
        labels[0] = 'Pb204/Pb206'
        labels[1] = 's[Pb204/Pb206]'
        labels[2] = 'Pb207/Pb206'
        labels[3] = 's[Pb207/Pb206]'
        labels[4] = 'rho[Pb204/Pb206,Pb207/Pb206]'
        out.columns = labels
        out.index = list(self.keys())
        return out

class Result(pd.DataFrame):

    def ages(self):
        pass

    def avg_Pb764(self):
        mu7 = np.mean(self['Pb7'])
        mu6 = np.mean(self['Pb6'])
        mu4 = np.mean(self['Pb4'])
        se7 = sp.stats.sem(self['Pb7'])
        se6 = sp.stats.sem(self['Pb6'])
        se4 = sp.stats.sem(self['Pb4'])
        Pb46 = mu4/mu6
        Pb76 = mu7/mu6
        J = np.array([[0,-mu4/mu6**2,1/mu6],
                      [1/mu6,-mu7/mu6**2,0]])
        E = np.diag([se7,se6,se4])**2
        covmat = J @ E @ np.transpose(J)
        se46 = np.sqrt(covmat[0,0])
        se76 = np.sqrt(covmat[1,1])
        rho = 0.0 if se46==0 or se76==0 else covmat[0,1]/(se46*se76)
        return [Pb46,se46,Pb76,se76,rho]
