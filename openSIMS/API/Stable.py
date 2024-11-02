import math
import pandas as pd
import numpy as np
import openSIMS as S
from . import Toolbox
from matplotlib.figure import Figure

class Stable:

    def get_cps(self,name):
        sample = self.samples.loc[name]
        settings = S.settings(self.method)
        ions = settings['ions']
        out = pd.DataFrame()
        for ion in ions:
            out[ion] = sample.cps(self.method,ion)['cps']
        return out

    def get_ratios(self):
        settings = S.settings(self.method)
        num, den = settings.get_num_den()
        ratios = settings.get_labels()
        return num, den, ratios

    def raw_logratios(self,name):
        num, den, ratios = self.get_ratios()
        raw_cps = self.get_cps(name)
        out = np.log(raw_cps[num]) - np.log(raw_cps[den]).values
        return out.set_axis(ratios,axis=1)

    def process(self):
        self.results = Results(self.method)
        for name, sample in self.samples.items():
            logratios = self.raw_logratios(name)
            deltap = logratios.apply(lambda lr: lr + self.pars, axis=1)
            self.results[name] = Result(deltap)

class Calibrator:

    def calibrate(self,**kwargs):
        df_list = []
        for name, standard in self.samples.items():
            logratios = self.raw_logratios(name)
            dprime = self.get_deltap_standard(name,multiplier=1).values
            df = logratios.apply(lambda lr: dprime - lr, axis=1)
            df_list.append(df)
        pooled = pd.concat(df_list)
        self.pars = pooled.mean(axis=0)

    def get_deltap_standard(self,name,multiplier=1000):
        num, den, ratios = self.get_ratios()
        standard = self.samples.loc[name]
        settings = S.settings(self.method)
        delta = settings['refmats'][ratios].loc[standard.group]
        return np.log(1+delta/1000)*multiplier

    def plot(self,fig=None,ax=None,show=False):
        num_panels = len(self.pars)
        ratio_names = self.pars.index.to_list()
        nr = math.ceil(math.sqrt(num_panels))
        nc = math.ceil(num_panels/nr)
        fig, ax = init_fig(fig,ax,num_panels,nr,nc)
        lines = dict()
        self.process()
        deltap = self.results.average()
        np.random.seed(1)
        for sname, standard in self.samples.items():
            group = standard.group
            if group in lines.keys():
                colour = lines[group]['colour']
            else:
                colour = np.random.rand(3,)
                lines[group] = dict()
                lines[group]['colour'] = colour
                if group != 'sample':
                    lines[group]['truth'] = self.get_deltap_standard(sname)
            for i, rname in enumerate(ratio_names):
                y = deltap.loc[sname,rname]
                sy = deltap.loc[sname,'s['+rname+']']
                ax[i].scatter(sname,y,s=5,color='black',zorder=2)
                ax[i].plot([sname,sname],[y-sy,y+sy],
                           '-',color=colour,zorder=1)
        for i, rname in enumerate(ratio_names):
            title = r"$\delta$'" + "(" + rname + ")"
            ax[i].set_title(title)
        for group, val in lines.items():
            if group != 'sample':
                for i, rname in enumerate(ratio_names):
                    ax[i].axline((0.0,val['truth'][rname]),
                                 slope=0.0,
                                 color=val['colour'],
                                 zorder=0)
        fig.tight_layout()
        if show: Toolbox.show_figure(fig)
        return fig, ax

class Processor:

    def plot(self,fig=None,ax=None,show=False):
        num_panels = len(self.pars)
        ratio_names = self.pars.index.to_list()
        nr = math.ceil(math.sqrt(num_panels))
        nc = math.ceil(num_panels/nr)
        fig, ax = init_fig(fig,ax,num_panels,nr,nc)
        deltap = self.results.average()
        for sname, standard in self.samples.items():
            for i, rname in enumerate(ratio_names):
                y = deltap.loc[sname,rname]
                sy = deltap.loc[sname,'s['+rname+']']
                ax[i].scatter(sname,y,s=5,color='black',zorder=2)
                ax[i].plot([sname,sname],[y-sy,y+sy],
                           '-',color='black',zorder=1)
        for i, rname in enumerate(ratio_names):
            title = r"$\delta$'" + "(" + rname + ")"
            ax[i].set_title(title)
        fig.tight_layout()
        if show: Toolbox.show_figure(fig)
        return fig, ax    
    
class Results(dict):

    def __init__(self,method):
        super().__init__()
        self.ratios = S.settings(method).get_labels()

    def average(self,multiplier=1000):
        lst = []
        for name, result in self.items():
            lst.append(result.average(multiplier=multiplier))
        out = pd.DataFrame(lst)
        nc = out.shape[1]
        nratios = len(self.ratios)
        labels = []
        rho_labels = []
        for i, ratio in enumerate(self.ratios):
            labels.append(ratio)
            labels.append('s[' + ratio + ']')
            for j in range(i+1,nratios):
                rho_labels.append('rho[' + ratio + ',' + self.ratios[j] + ']')
        out.columns = labels + rho_labels
        out.index = list(self.keys())
        return out

class Result(pd.DataFrame):

    def delta(self):
        pass

    def average(self,multiplier=1):
        avg = np.mean(self,axis=0)
        nr = self.shape[0]
        nc = self.shape[1]
        covmat = self.cov()/nr
        cormat = self.corr()
        out = []
        for i, val in enumerate(avg):
            out.append(avg.iloc[i]*multiplier)
            out.append(np.sqrt(covmat.iloc[i,i])*multiplier)
        rho = cormat.iloc[np.triu_indices(nc,k=1)].values.flatten()
        return np.hstack((out,rho))

def init_fig(fig,ax,num_panels,nr,nc):
    if fig is None or ax is None:
        fig = Figure()
        ax = [None]*num_panels
        for i in range(num_panels):
            ax[i] = fig.add_subplot(nr,nc,i+1)
    return fig, ax