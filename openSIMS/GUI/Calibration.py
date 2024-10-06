import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from . import Main
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CalibrationWindow(tk.Toplevel):

    def __init__(self,top,button):
        super().__init__()
        self.title('Calibration')
        top.set_method()
        self.top = top
        Main.offset(button,self)

        fig = plt.figure(top.figures['calibration'])
        self.canvas = FigureCanvasTkAgg(fig,master=self)
        self.canvas.get_tk_widget().pack(expand=tk.TRUE,fill=tk.BOTH)
        self.canvas.figure, axs = S.plot_calibration()
        self.canvas.draw()

        self.var = tk.StringVar()
        self.combo = ttk.Combobox(self,
                                  values=S.list_methods(),
                                  textvariable=self.var)
        self.var.set(self.top.method)
        self.combo.pack(pady=2)
        
        self.protocol("WM_DELETE_WINDOW",self.on_closing)

    def on_closing(self):
        self.top.calibration_window = None
        self.destroy()

    def on_change(self,event):
        pass
