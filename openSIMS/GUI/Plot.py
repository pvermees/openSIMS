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
        self.add_canvas()
        self.add_combo()
        self.protocol("WM_DELETE_WINDOW",self.on_closing)

    def add_canvas(self):
        fig, axs = self.action(self.master.method)
        self.canvas = FigureCanvasTkAgg(fig,master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
        self.canvas.draw()

    def add_combo(self):
        methods = S.list_methods()
        if len(methods)>1:
            self.combolabel = ttk.Label(self,text='Methods:')
            self.combolabel.pack(expand=tk.TRUE,side=tk.LEFT,pady=2)
            self.var = tk.StringVar()
            self.combo = ttk.Combobox(self,values=methods,
                                      textvariable=self.var,
                                      width=10)
            self.combo.bind("<<ComboboxSelected>>",self.on_change)
            self.var.set(self.master.method)
            self.combo.pack(expand=tk.TRUE,side=tk.LEFT,pady=2)

    def on_change_helper(self):
        self.master.method = self.combo.get()
        self.canvas.get_tk_widget().pack_forget()
        self.combolabel.pack_forget()
        self.combo.pack_forget()
        self.add_canvas()
        self.add_combo()

    def on_closing(self):
        setattr(self.master,self.window_id,None)
        self.destroy()

class CalibrationWindow(PlotWindow):

    def __init__(self,top,button):
        super().__init__(top,button,
                         title='Calibration',
                         figure_type='calibration',
                         action=S.plot_calibration,
                         window_id='calibration_window')
        methods = S.list_methods()
        if len(methods)>1:
            self.add_entries()

    def add_entries(self):
        self.master.method = self.combo.get()
        fixable = self.get_fixable()
        self.labels = dict()
        self.entries = dict()
        for key in fixable:
            self.labels[key] = ttk.Label(self,text=key+':')
            self.labels[key].pack(expand=tk.TRUE,side=tk.LEFT,pady=2)
            self.entries[key] = ttk.Entry(self,width=5)
            txt = self.get_fixed_entry(fixable[key])
            self.entries[key].insert(0,txt)
            self.entries[key].pack(expand=tk.TRUE,side=tk.LEFT,pady=2)
        self.button = ttk.Button(self,text='Recalibrate')
        self.button.bind("<Button-1>",self.recalibrate)
        self.button.pack(expand=True,fill=tk.BOTH)

    def get_fixed_entry(self,par):
        self.master.method = self.combo.get()
        fixed = S.get('fixed')
        if self.master.method in fixed and par in fixed[self.master.method]:
            return fixed[self.master.method][par]
        else:
            return 'auto'

    def refresh_entries(self):
        for key in self.entries:
            self.labels[key].pack_forget()
            self.entries[key].pack_forget()
        self.button.pack_forget()
        self.add_entries()

    def get_fixable(self):
        method = S.settings()[self.master.method]
        if method['type'] == 'geochron':
            return {'slope': 'B', 'drift': 'b'}
        elif method['type'] == 'geochron_PbPb':
            return {'massfrac': 'a', 'drift': 'b'}
        elif method['type'] == 'stable':
            return None

    def on_change(self,event):
        self.on_change_helper()
        self.refresh_entries()

    def recalibrate(self,event):
        fixable = self.get_fixable()
        args = []
        for par, entry in self.entries.items():
            val = entry.get()
            if val == 'auto':
                pass
            else:
                args.append(fixable[par] + '=' + val)
        if len(args)>0:
            fixcmd = "S.fix_pars('" + self.master.method + "'," + ','.join(args) + ")"
            calcmd = "S.calibrate('" + self.master.method + "')"
        else:
            fixcmd = "S.unfix_pars('" + self.master.method + "')"
            calcmd = "S.calibrate()"
        self.master.run(fixcmd)
        self.master.run(calcmd)
        self.on_change(event)

class ProcessWindow(PlotWindow):

    def __init__(self,top,button):
        super().__init__(top,
                         button,
                         title='Samples',
                         figure_type='process',
                         action=S.plot_processed,
                         window_id='process_window')

    def on_change(self,event):
        self.on_change_helper()