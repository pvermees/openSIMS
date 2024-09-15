import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from . import Main
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

class PlotWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__()
        self.title('Plot')
        Main.offset(top,self)
        fig, axs = S.plot(show=False,num=top.figs[0])
  
        canvas = FigureCanvasTkAgg(fig,master=self)
        canvas.get_tk_widget().pack(expand=tk.TRUE,fill=tk.BOTH)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
  
        previous_button = ttk.Button(self,text='<',
                                     command=lambda c=canvas,t=top:
                                     self.plot_previous(t,c))
        previous_button.pack(expand=tk.TRUE,side=tk.LEFT)
        next_button = ttk.Button(self,text='>',
                                 command=lambda c=canvas,t=top:
                                 self.plot_next(t,c))
        next_button.pack(expand=tk.TRUE,side=tk.LEFT)

    def plot_previous(self,top,canvas):
        self.refresh_canvas(top,canvas,-1)

    def plot_next(self,top,canvas):
        self.refresh_canvas(top,canvas,+1)

    def refresh_canvas(self,top,canvas,di):
        ns = len(S.get('samples'))
        i = (S.get('i') + di) % ns
        S.set('i',i)
        canvas.figure.clf()
        canvas.figure, axs = S.plot(show=False,num=top.figs[0])
        canvas.draw()
