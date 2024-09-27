import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import openSIMS as S
from abc import ABC, abstractmethod

class Sample(ABC):

    def __init__(self):
        self.date = None
        self.time = pd.DataFrame()
        self.signal = pd.DataFrame()
        self.sbm = pd.DataFrame()
        self.channels = pd.DataFrame()
        self.detector = pd.DataFrame()
        self.group = 'sample'

    @abstractmethod
    def read(self,fname):
        pass

    @abstractmethod
    def cps(self,ion):
        pass

    def view(self,channels=None,title=None,show=True,num=None):
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
                ax[r,c].scatter(self.time[channel],self.signal[channel])
                ax[r,c].set_title(channel)
        if show:
            plt.show()
        return fig, ax

    def offset(self,method):
        method = S.settings(method)
        DP = method.get_DP(self.group)
        L = method['lambda']
        y0t = np.log(DP)
        y01 = np.log(np.exp(L)-1)
        return y0t - y01
    
    def calibration_data_UPb(self,b):
        U = self.cps('U')
        UOx = self.cps('UOx')
        Pb4 = self.cps('Pb204')
        Pb6 = self.cps('Pb206')
        drift = np.exp(b*Pb6['time']/60)
        a0 = S.settings('U-Pb').get_a0(self.group)
        x = np.log(UOx['cps']) - np.log(U['cps'])
        y = np.log(drift*Pb6['cps']-a0*Pb4['cps']) - np.log(U['cps'])
        return x, y
