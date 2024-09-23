import pandas as pd
import tkinter as tk
import numpy as np
import glob
import os
from . import Cameca, Refmats, Crunch
from pathlib import Path
from scipy.optimize import minimize

class simplex:
    
    def __init__(self):
        self.reset()
        self.i = 0
        self.header = 'import openSIMS as S'
        self.stack = [self.header]

    def reset(self):
        self.instrument = None
        self.path = None
        self.method = None
        self.samples = None
        self.ignore = set()
        self.pars = None

    def read(self):
        self.samples = pd.Series()
        if self.instrument == 'Cameca':
            fnames = glob.glob(os.path.join(self.path,'*.asc'))
            for fname in fnames:
                sname = Path(fname).stem
                self.samples[sname] = Cameca.Cameca_Sample()
                self.samples[sname].read(fname)
        elif self.instrument == 'SHRIMP':
            self.TODO(self)
        else:
            raise ValueError('Unrecognised instrument type.')
        self.sort_samples()

    def process(self):
        standards = self.get_standards()
        res = minimize(Crunch.misfit,0.0,
                       method='nelder-mead',
                       args=(standards))
        b = res.x[0]
        x, y = Crunch.getxy(b,standards)
        A, B = Crunch.linearfit(x,y)
        self.pars = {'A':A, 'B':B, 'b':b}

    def get_standards(self):
        out = dict()
        for sname, sample in self.samples.items():
            if sample.group != 'sample':
                out[sname] = sample
        return out

    def sort_samples(self):
        order = np.argsort(self.get_dates())
        new_index = self.samples.index[order.tolist()]
        self.samples = self.samples.reindex(index=new_index)

    def get_dates(self):
        dates = np.array([])
        for name, sample in self.samples.items():
            dates = np.append(dates,sample.date)
        return dates

    def plot(self,i=None,sname=None,show=True,num=None):
        snames = self.samples.index
        if sname in snames:
            self.i = snames.index(sname)
        else:
            if i is not None:
                self.i = i % len(snames)
            sname = snames[self.i]
        return self.samples[sname].plot(title=sname,show=show,num=num)

    def channels(self):
        run = self.samples
        if len(run)>0:
            return self.samples.iloc[0].channels.index.tolist()
        else:
            return None

    def get_groups(self):
        out = set()
        for sample in self.samples:
            out.add(sample.group)
        return out
        
    def set_groups(self,**kwargs):
        for key, sample in self.samples.items():
            sample.group = 'sample'
        for name, indices in kwargs.items():
            for i in indices:
                self.samples.iloc[i].group = name

    def TODO(self):
        pass
