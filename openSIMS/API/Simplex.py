import os
import glob
import math
import pkgutil
import importlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from . import Cameca, Calibration, Process
from .. import Methods
from pathlib import Path

class Simplex:
    
    def __init__(self):
        self.reset()
        self.i = 0
        self.header = 'import openSIMS as S'
        self.stack = [self.header]

    def reset(self):
        self.instrument = None
        self.path = None
        self.samples = None
        self.ignore = set()
        self.methods = dict()
        self.pars = dict()
        self.results = dict()

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
        self.check_method()

    def check_method(self):
        all_channels = self.all_channels()
        for method, channels in self.methods.items():
            method_channels = channels.values()
            if not set(method_channels).issubset(all_channels):
                self.methods = dict()
                self.pars = dict()
                self.results = dict()
                return

    def hasMethods(self,methods):
        return set(methods).issubset(set(self.methods.keys()))

    def calibrate(self):
        for method, channels in self.methods.items():
            standards = Calibration.get_standards(self,method)
            standards.calibrate()
            self.pars[method] = standards.pars

    def process(self):
        for method, channels in self.methods.items():
            samples = Process.get_samples(self,method)
            samples.process()
            self.results[method] = samples.results

    def sort_samples(self):
        order = np.argsort(self.get_dates())
        new_index = self.samples.index[order.tolist()]
        self.samples = self.samples.reindex(index=new_index)

    def get_dates(self):
        dates = np.array([])
        for name, sample in self.samples.items():
            dates = np.append(dates,sample.date)
        return dates

    def view(self,i=None,sname=None):
        snames = self.samples.index
        if sname in snames:
            self.i = snames.index(sname)
        else:
            if i is not None:
                self.i = i % len(snames)
            sname = snames[self.i]
        return self.samples[sname].view(title=sname)

    def plot_calibration(self,method=None):
        toplot = Calibration.get_standards(self,method)
        return toplot.plot()

    def plot_processed(self,method=None):
        toplot = Process.get_samples(self,method)
        return toplot.plot()

    def all_channels(self):
        run = self.samples
        if len(run)>0:
            return run.iloc[0].channels.index.tolist()
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
                self.get_sample(i).group = name

    def get_sample(self,identifier):
        if type(identifier) is int:
            return self.samples.iloc[identifier]
        elif type(identifier) is str:
            return self.samples[identifier]
        else:
            raise ValueError('Invalid sample identifier')

    def get_pars(self,method):
        if method in self.pars.keys():
            return self.pars[method]
        else:
            return dict()

    def exporters(self):
        import openSIMS.Methods.Exporters
        exporters = pkgutil.iter_modules(openSIMS.Methods.Exporters.__path__)
        return [name for importer, name, ispkg in exporters]

    def export_timeresolved(self,path):
        pass

    def export_csv(self,path,fmt='default'):
        if len(self.results) > 0:
            module_name = 'openSIMS.Methods.Exporters.' + fmt
            module = importlib.import_module(module_name)
            module.csv(self,path)
        else:
            raise ValueError("This dataset hasn't been processed yet")

    def export_json(self,path):
        pass
    
    def TODO(self):
        pass
