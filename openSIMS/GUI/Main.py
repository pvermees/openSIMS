import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
from . import Doc, Export, List, Log, Method, Open, Plot, View

class gui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('openSIMS')
        self.figures = {'view':100,'calibration':101,'process':102}
        self.method = None
        self.open_window = None
        self.method_window = None
        self.log_window = None
        self.list_window = None
        self.view_window = None
        self.calibration_window = None
        self.process_window = None
        self.export_window = None
        self.help_window = None
        self.create_open_button()
        self.create_method_button()
        self.create_view_button()
        self.create_standard_button()
        self.create_calibrate_button()
        self.create_process_button()
        self.create_export_button()
        self.create_log_button()
        self.create_template_button()
        self.create_settings_button()
        self.create_help_button()
        self.exporter = 'default'

    def run(self,cmd):
        S.get('stack').append(cmd)
        exec(cmd)
        if self.log_window is not None:
            self.log_window.log(cmd=cmd)

    def create_open_button(self):
        button = ttk.Button(self,text='Open')
        button.bind("<Button-1>", self.on_open)
        button.pack(expand=True,fill=tk.BOTH)

    def create_method_button(self):
        button = ttk.Button(self,text='Method')
        button.bind("<Button-1>", self.on_method)
        button.pack(expand=True,fill=tk.BOTH)

    def create_view_button(self):
        button = ttk.Button(self,text='View')
        button.bind("<Button-1>", self.on_view)
        button.pack(expand=True,fill=tk.BOTH)

    def create_standard_button(self):
        button = ttk.Button(self,text='Standards')
        button.bind("<Button-1>", self.on_standard)
        button.pack(expand=True,fill=tk.BOTH)

    def create_calibrate_button(self):
        button = ttk.Button(self,text='Calibrate')
        button.bind("<Button-1>", self.on_calibrate)
        button.pack(expand=True,fill=tk.BOTH)

    def create_process_button(self):
        button = ttk.Button(self,text='Process')
        button.bind("<Button-1>", self.on_process)
        button.pack(expand=True,fill=tk.BOTH)
        
    def create_export_button(self):
        button = ttk.Button(self,text='Export')
        button.bind("<Button-1>", self.on_export)
        button.pack(expand=True,fill=tk.BOTH)

    def create_log_button(self):
        button = ttk.Button(self,text='Log')
        button.bind("<Button-1>", self.on_log)
        button.pack(expand=True,fill=tk.BOTH)

    def create_template_button(self):
        button = ttk.Button(self,text='Template')
        button.bind("<Button-1>", self.on_template)
        button.pack(expand=True,fill=tk.BOTH)

    def create_settings_button(self):
        button = ttk.Button(self,text='Settings')
        button.bind("<Button-1>", self.on_settings)
        button.pack(expand=True,fill=tk.BOTH)

    def create_help_button(self):
        button = ttk.Button(self,text='Help')
        button.bind("<Button-1>", self.on_help)
        button.pack(expand=True,fill=tk.BOTH)

    def on_open(self,event):
        if self.open_window is None:
            self.open_window = Open.OpenWindow(self,event.widget)
        else:
            self.open_window.destroy()
            self.open_window = None

    def is_empty(self):
        if S.get('samples') is None:
            tk.messagebox.showwarning(message='No data')
            return True
        else:
            return False

    def on_method(self,event):
        if self.is_empty(): return
        if self.method_window is None:
            self.method_window = Method.MethodWindow(self,event.widget)
        else:
            self.method_window.destroy()
            self.method_window = None

    def set_method_if_None(self):
        if self.method is None and len(S.get('methods'))>0:
            self.method = S.list_methods()[0]

    def on_standard(self,event):
        if self.is_empty(): return
        if self.list_window is None:
            self.list_window = List.ListWindow(self,event.widget)
        else:
            self.list_window.destroy()
            self.list_window = None

    def on_calibrate(self,event):
        if self.is_empty(): return
        if self.calibration_window is None:
            self.run("S.calibrate()")
            self.calibration_window = Plot.CalibrationWindow(self,event.widget)
        else:
            self.calibration_window.destroy()
            self.calibration_window = None

    def on_process(self,event):
        if self.is_empty(): return
        if self.process_window is None:
            self.run("S.process()")
            self.process_window = Plot.ProcessWindow(self,event.widget)
        else:
            self.process_window.destroy()
            self.process_window = None

    def on_export(self,event):
        if self.is_empty(): return
        if self.export_window is None:
            self.export_window = Export.ExportWindow(self,event.widget)
        else:
            self.export_window.destroy()
            self.export_window = None

    def on_view(self,event):
        if self.is_empty(): return
        if self.view_window is None and len(S.get('samples'))>0:
            self.view_window = View.ViewWindow(self,event.widget)
        else:
            self.view_window.destroy()
            self.view_window = None

    def on_log(self,event):
        if self.log_window is None:
            self.log_window = Log.LogWindow(self,event.widget)
            self.log_window.show()
        else:
            self.log_window.destroy()
            self.log_window = None

    def on_template(self,event):
        self.run("S.TODO()")

    def on_settings(self,event):
        self.run("S.TODO()")

    def on_help(self,event):
        if self.help_window is None:
            self.help_window = Doc.HelpWindow(self,event.widget,item='top')
        else:
            self.help_window.destroy()
            self.help_window = None

def offset(parent,child):
    x_offset = parent.winfo_rootx()
    width = parent.winfo_width()
    y_offset = parent.winfo_rooty()
    child.geometry("+{}+{}".format(x_offset+width, y_offset))
