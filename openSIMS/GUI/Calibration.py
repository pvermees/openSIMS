import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from . import Main
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

class CalibrationWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__()
        self.title('Calibration')
        self.top = top
        fig, axs = S.plot()
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
        self.canvas.figure, axs = S.plot()
        self.canvas.draw()

    def on_closing(self):
        self.top.calibration_window = None
        self.destroy()
