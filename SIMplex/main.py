import SIMplex
from pathlib import Path
import pandas as pd
import glob
import os

class simplex:
    
    def __init__(self,gui=False):
        self.reset()
        if gui: self.gui = SIMplex.gui(self)

    def reset(self):
        self.instrument = None
        self.path = None
        self.method = None
        self.samples = pd.Series()

    def set_instrument(self,instrument):
        self.instrument = instrument
    def get_instrument(self):
        return(self.instrument)

    def set_path(self,path):
        self.path = path
    def get_path(self):
        return(self.path)

    def read(self):
        if self.instrument == 'Cameca':
            fnames = glob.glob(os.path.join(self.path,'*.asc'))
            for fname in fnames:
                sname = Path(fname).stem
                self.samples[sname] = SIMplex.Cameca_Sample()
                self.samples[sname].read(fname)
        elif self.instrument == 'SHRIMP':
            todo(self)
        else:
            raise ValueError('Unrecognised instrument type.')

    def plot(self,i=1,sname=None):
        snames = self.samples.index
        if sname not in snames:
            sname = snames[i % len(snames)]
        self.samples[sname].plot()
            
    def TODO(self):
        pass
