import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from . import Main
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

class ViewWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__()
        self.title('View')
        Main.offset(top,self)
        fig, axs = S.view()
  
        canvas = FigureCanvasTkAgg(fig,master=self)
        canvas.get_tk_widget().pack(expand=tk.TRUE,fill=tk.BOTH)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
  
        previous_button = ttk.Button(self,text='<',
                                     command=lambda c=canvas,t=top:
                                     self.view_previous(t,c))
        previous_button.pack(expand=tk.TRUE,side=tk.LEFT)
        next_button = ttk.Button(self,text='>',
                                 command=lambda c=canvas,t=top:
                                 self.view_next(t,c))
        next_button.pack(expand=tk.TRUE,side=tk.LEFT)

    def view_previous(self,top,canvas):
        self.refresh_canvas(top,canvas,-1)

    def view_next(self,top,canvas):
        self.refresh_canvas(top,canvas,+1)

    def refresh_canvas(self,top,canvas,di):
        ns = len(S.get('samples'))
        i = (S.get('i') + di) % ns
        S.set('i',i)
        canvas.figure.clf()
        canvas.figure, axs = S.view()
        canvas.draw()
