import openSIMS as S
from pathlib import Path
import pandas as pd
import tkinter as tk
import glob
import os

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
        self.samples = pd.Series()

    def read(self):
        if self.instrument == 'Cameca':
            fnames = glob.glob(os.path.join(self.path,'*.asc'))
            for fname in fnames:
                sname = Path(fname).stem
                self.samples[sname] = S.Cameca.Cameca_Sample()
                self.samples[sname].read(fname)
        elif self.instrument == 'SHRIMP':
            self.TODO(self)
        else:
            raise ValueError('Unrecognised instrument type.')

    def plot(self,i=None,sname=None,show=True,num=None):
        snames = self.samples.index
        if sname in snames:
            self.i = snames.index(sname)
        else:
            if i is not None:
                self.i = i % len(snames)
            sname = snames[self.i]
        return self.samples[sname].plot(title=sname,show=show,num=num)
            
    def TODO(self):
        pass
