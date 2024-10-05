import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from . import Main
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CalibrationWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__()
        self.title('Calibration')
        self.top = top
        Main.offset(self.top,self)

        fig = plt.figure(top.figures['calibration'])
        canvas = FigureCanvasTkAgg(fig,master=self)
        canvas.get_tk_widget().pack(expand=tk.TRUE,fill=tk.BOTH)
        canvas.figure, axs = S.plot_calibration()
        canvas.draw()

        self.protocol("WM_DELETE_WINDOW",self.on_closing)

    def on_closing(self):
        self.top.calibration_window = None
        self.destroy()
