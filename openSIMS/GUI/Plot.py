import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.figure import Figure
from . import Main
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotWindow(tk.Toplevel):

    def __init__(self,top,button,title=None,
                 figure_type=None,action=None,window_id=None):
        super().__init__(top)
        self.title(title)
        top.set_method_if_None()
        self.action = action
        self.window_id = window_id
        Main.offset(button,self)

        fig, axs = action(self.master.method)

        self.canvas = FigureCanvasTkAgg(fig,master=self)
        self.canvas.get_tk_widget().pack(expand=tk.TRUE,fill=tk.BOTH)
        self.canvas.draw()

        methods = S.list_methods()
        if len(methods)>1:
            label = ttk.Label(self,text='Methods:')
            label.pack(expand=tk.TRUE,side=tk.LEFT,pady=2)
            self.var = tk.StringVar()
            self.combo = ttk.Combobox(self,values=methods,
                                      textvariable=self.var,
                                      width=10)
            self.combo.bind("<<ComboboxSelected>>",self.on_change)
            self.var.set(self.master.method)
            self.combo.pack(expand=tk.TRUE,side=tk.LEFT,pady=2)

        self.protocol("WM_DELETE_WINDOW",self.on_closing)

    def on_closing(self):
        setattr(self.master,self.window_id,None)
        self.destroy()
        
    def on_change(self,event):
        self.master.method = self.combo.get()
        self.canvas.figure.clf()
        self.canvas.figure, axs = self.action(self.master.method)
        self.canvas.draw()

class CalibrationWindow(PlotWindow):

    def __init__(self,top,button):
        super().__init__(top,button,
                         title='Calibration',
                         figure_type='calibration',
                         action=S.plot_calibration,
                         window_id='calibration_window')
        
        current_method = self.combo.get()
        fixable = self.get_fixable(current_method)
        self.entries = dict()
        self.labels = dict()
        for key in fixable:
            self.labels[key] = ttk.Label(self,text=key+':')
            self.labels[key].pack(expand=tk.TRUE,side=tk.LEFT,pady=2)
            self.entries[key] = ttk.Entry(self,width=5)
            self.entries[key].insert(0,"auto")
            self.entries[key].pack(expand=tk.TRUE,side=tk.LEFT,pady=2)
        button = ttk.Button(self,text='Recalibrate')
        button.bind("<Button-1>", self.recalibrate)
        button.pack(expand=True,fill=tk.BOTH)

    def get_fixable(self,method_name):
        method = S.settings()[method_name]
        if method['type'] == 'geochron':
            return {'slope': 'B', 'drift': 'b'}
        elif method['type'] == 'geochron_PbPb':
            return {'mass fractionation': 'a', 'drift': 'b'}
        elif method['type'] == 'stable':
            return None

    def recalibrate(self,event):
        pass

class ProcessWindow(PlotWindow):

    def __init__(self,top,button):
        super().__init__(top,
                         button,
                         title='Samples',
                         figure_type='process',
                         action=S.plot_processed,
                         window_id='process_window')
