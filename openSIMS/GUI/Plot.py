import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from . import Main
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotWindow(tk.Toplevel):

    def __init__(self,top,button,title=None,
                 figure_type=None,action=None,window_id=None):
        super().__init__()
        self.title(title)
        top.set_method_if_None()
        self.top = top
        self.action = action
        self.window_id = window_id
        Main.offset(button,self)

        fig = plt.figure(top.figures[figure_type])
        self.canvas = FigureCanvasTkAgg(fig,master=self)
        self.canvas.get_tk_widget().pack(expand=tk.TRUE,fill=tk.BOTH)
        self.canvas.figure, axs = action(self.top.method)
        self.canvas.draw()

        methods = S.list_methods()
        if len(methods)>1:
            label = ttk.Label(self,text='Methods:')
            label.pack(expand=tk.TRUE,side=tk.LEFT,pady=2)
            self.var = tk.StringVar()
            self.combo = ttk.Combobox(self,values=methods,
                                      textvariable=self.var)
            self.combo.bind("<<ComboboxSelected>>",self.on_change)
            self.var.set(self.top.method)
            self.combo.pack(expand=tk.TRUE,side=tk.LEFT,pady=2)

        self.protocol("WM_DELETE_WINDOW",self.on_closing)

    def on_closing(self):
        self.window_id = None
        self.destroy()
        
    def on_change(self,event):
        self.top.method = self.combo.get()
        self.canvas.figure.clf()
        self.canvas.figure, axs = self.action(self.top.method)
        self.canvas.draw()

class CalibrationWindow(PlotWindow):

    def __init__(self,top,button):
        super().__init__(top,button,
                         title='Calibration',
                         figure_type='calibration',
                         action=S.plot_calibration,
                         window_id=top.calibration_window)
        
class ProcessWindow(PlotWindow):

    def __init__(self,top,button):
        super().__init__(top,
                         button,
                         title='Samples',
                         figure_type='process',
                         action=S.plot_processed,
                         window_id=top.process_window)
