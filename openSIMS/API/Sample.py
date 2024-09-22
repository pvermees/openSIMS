import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from . import Crunch, Refmats
from scipy.optimize import minimize

class Sample:

    def __init__(self):
        self.date = None
        self.time = pd.DataFrame()
        self.signal = pd.DataFrame()
        self.sbm = pd.DataFrame()
        self.channels = pd.DataFrame()
        self.detector = pd.DataFrame()
        self.group = 'sample'

    def misfit_data_UPb(self):
        U = self.cps('U')
        UO = self.cps('UO')
        Pb4 = self.cps('Pb204')
        Pb6 = self.cps('Pb206')
        return U['cps'], UO['cps'], Pb4['cps'], Pb6['cps'], Pb6['time']

    def plot(self,channels=None,title=None,show=True,num=None):
        if channels is None:
            channels = self.signal.columns
        nr = math.ceil(math.sqrt(len(channels)))
        nc = math.ceil(len(channels)/nr)
        fig, ax = plt.subplots(nr,nc,num=num)
        if title is not None:
            plt.suptitle(title)
        for r in range(nr):
            for c in range(nc):
                channel = channels[r*nc+c]
                ax[r,c].plot(self.time[channel],self.signal[channel])
                ax[r,c].set_title(channel)
        if show:
            plt.show()
        return fig, ax
