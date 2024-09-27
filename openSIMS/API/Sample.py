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
        np = len(channels)
        nr = math.ceil(math.sqrt(np))
        nc = math.ceil(np/nr)
        fig, ax = plt.subplots(nr,nc,num=num)
        if title is not None:
            plt.suptitle(title)
        for r in range(nr):
            for c in range(nc):
                i = r*nc+c
                if i==np:
                    break
                else:
                    channel = channels[i]
                    ax[r,c].scatter(self.time[channel],self.signal[channel])
                    ax[r,c].set_title(channel)
        if show:
            plt.show()
        return fig, ax
