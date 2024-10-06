import openSIMS as S
import tkinter as tk
import matplotlib.pyplot as plt
from . import Main
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SamplesWindow(tk.Toplevel):
    
    def __init__(self,top,button):
        super().__init__()
        self.title('Samples')
        self.top = top
        Main.offset(button,self)

        fig = plt.figure(top.figures['process'])
        canvas = FigureCanvasTkAgg(fig,master=self)
        canvas.figure, axs = S.plot_processed()
        canvas.get_tk_widget().pack(expand=tk.TRUE,fill=tk.BOTH)
        canvas.draw()
        
        self.protocol("WM_DELETE_WINDOW",self.on_closing)
  
    def on_closing(self):
        self.top.samples_window = None
        self.destroy()
