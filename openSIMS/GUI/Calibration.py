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
        Main.offset(top,self)
        fig, axs = S.plot(show=False,num=top.figs[1])
  
        canvas = FigureCanvasTkAgg(fig,master=self)
        canvas.get_tk_widget().pack(expand=tk.TRUE,fill=tk.BOTH)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
  
    def refresh(self,top,canvas,di):
        S.set('i',i)
        canvas.figure.clf()
        canvas.figure, axs = S.view(show=False,num=top.figs[1])
        canvas.draw()
