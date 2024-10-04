import copy
import math
import numpy as np
import pandas as pd
import openSIMS as S
import matplotlib.pyplot as plt
from . import Toolbox, Sample, Ellipse
from scipy.optimize import minimize
from abc import ABC, abstractmethod

def getSamples(simplex,method=None):
    if method is None:
        method = list(simplex.methods.keys())[0]
    datatype = S.settings(method)['type']
    if datatype == 'geochron':
        return GeochronSamples(simplex,method)
    elif datatype == 'stable':
        return StableSamples(simplex,method)
    else:
        raise ValueError('Unrecognised data type')

class Samples(ABC):

    def __init__(self,simplex,method,omit_standards=True):
        self.pars = simplex.get_pars(method)
        self.method = method
        self.samples = copy.copy(simplex.samples)
        for sname, sample in simplex.samples.items():
            if sample.group != 'sample' and omit_standards:
                self.samples.drop(sname,inplace=True)

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def plot(self,fig=None,ax=None):
        pass

class GeochronSamples(Samples):

    def __init__(self,simplex,method):
        super().__init__(simplex,method)
    
    def process(self):
        p = self.pars
        return None
    
    def plot(self,fig=None,ax=None):
        return fig, ax

class StableSamples(Samples):

    def __init__(self,simplex,method):
        super().__init__(simplex,method)
    
    def process(self):
        p = self.pars
    
    def plot(self,fig=None,ax=None):
        return fig, ax
