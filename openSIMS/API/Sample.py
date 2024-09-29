import matplotlib.pyplot as plt
import pandas as pd
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

    def view(self,channels=None,title=None):
        if channels is None:
            channels = self.signal.columns
        num_panels = len(channels)
        nr = math.ceil(math.sqrt(num_panels))
        nc = math.ceil(num_panels/nr)
        fig, ax = plt.subplots(nr,nc)
        if title is not None:
            plt.suptitle(title)
        for i, channel in enumerate(channels):
            ax.ravel()[i].scatter(self.time[channel],self.signal[channel])
            ax.ravel()[i].set_title(channel)
        for empty_axis in range(len(channels),nr*nc):
            fig.delaxes(ax.flatten()[empty_axis])
        plt.subplots_adjust(left=0.1,top=0.9,right=0.9,bottom=0.1,
                            hspace=0.5,wspace=0.5)
        return fig, ax
