import openSIMS as S
import tkinter as tk
from . import Main
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

class SamplesWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__()
        self.title('Samples')
        self.top = top
        fig, axs = S.plot(show=False,calibration=False)
        self.canvas = FigureCanvasTkAgg(fig,master=self)
        self.canvas.get_tk_widget().pack(expand=tk.TRUE,fill=tk.BOTH)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas,self)
        self.toolbar.update()
        Main.offset(self.top,self)
        self.refresh()
        self.protocol("WM_DELETE_WINDOW",self.on_closing)
  
    def refresh(self):
        self.canvas.figure.clf()
        self.canvas.figure, axs = S.plot(show=False,calibration=False)
        self.canvas.draw()

    def on_closing(self):
        self.top.samples_window = None
        self.destroy()
