import pandas as pd
import math
from . import Toolbox
from matplotlib.figure import Figure
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
    def cps(self,method,ion):
        pass

    def total_time(self,method,channels):
        dwelltime = self.channels.loc[channels,'dwelltime']
        num_cycles = self.signal.shape[0]
        return dwelltime*num_cycles

    def view(self,channels=None,title=None,show=False):
        if channels is None:
            channels = self.signal.columns
        num_panels = len(channels)
        nr = math.ceil(math.sqrt(num_panels))
        nc = math.ceil(num_panels/nr)
        fig = Figure()
        ax = [None]*num_panels
        if title is not None:
            fig.suptitle(title)
        for i, channel in enumerate(channels):
            ax[i] = fig.add_subplot(nr,nc,i+1)
            ax[i].scatter(self.time[channel],self.signal[channel])
            ax[i].set_title(channel)
        if show: Toolbox.show_figure(fig)
        return fig, ax
