import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
from . import Doc, List, Log, Method, View, Calibration

class gui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('openSIMS')
        self.log_window = None
        self.list_window = None
        self.view_window = None
        self.calibration_window = None
        self.help_window = None
        self.create_open_button()
        self.create_method_button()
        self.create_view_button()
        self.create_standard_button()
        self.create_calibrate_button()
        self.create_export_button()
        self.create_log_button()
        self.create_template_button()
        self.create_settings_button()
        self.create_help_button()

    def run(self,cmd):
        S.get('stack').append(cmd)
        exec(cmd)
        if self.log_window is not None:
            self.log_window.log(cmd=cmd)

    def create_open_button(self):
        button = ttk.Menubutton(self,text='Open',direction='right')
        menu = tk.Menu(button,tearoff=0)
        for inst in ['Cameca','SHRIMP']:
            menu.add_command(label=inst,command=lambda i=inst: self.on_open(i))
        button["menu"] = menu
        button.pack(expand=True,fill=tk.BOTH)

    def create_method_button(self):
        button = ttk.Menubutton(self,text='Method',direction='right')
        menu = tk.Menu(button,tearoff=0)
        for method in ['U-Pb','Th-Pb','O','S']:
            menu.add_command(label=method,
                             command=lambda m=method: self.on_method(m))
            button["menu"] = menu
            button.pack(expand=True,fill=tk.BOTH)

    def create_view_button(self):
        button = ttk.Button(self,text='View',command=self.on_view)
        button.pack(expand=True,fill=tk.BOTH)

    def create_standard_button(self):
        button = ttk.Button(self,text='Standards',command=self.on_standard)
        button.pack(expand=True,fill=tk.BOTH)

    def create_calibrate_button(self):
        button = ttk.Button(self,text='Calibrate',command=self.on_calibrate)
        button.pack(expand=True,fill=tk.BOTH)

    def create_export_button(self):
        button = ttk.Button(self,text='Export',command=self.on_export)
        button.pack(expand=True,fill=tk.BOTH)

    def create_log_button(self):
        button = ttk.Button(self,text='Log',command=self.toggle_log_window)
        button.pack(expand=True,fill=tk.BOTH)

    def create_template_button(self):
        button = ttk.Button(self,text='Template',command=self.on_template)
        button.pack(expand=True,fill=tk.BOTH)

    def create_settings_button(self):
        button = ttk.Button(self,text='Settings',command=self.on_settings)
        button.pack(expand=True,fill=tk.BOTH)

    def create_help_button(self):
        button = ttk.Button(self,text='Help',command=self.on_help)
        button.pack(expand=True,fill=tk.BOTH)

    def on_open(self,inst):
        self.run("S.set('instrument','{i}')".format(i=inst))
        path = fd.askdirectory() if inst=='Cameca' else fd.askopenfile()
        self.run("S.set('path','{p}')".format(p=path))
        self.run("S.read()")

    def on_method(self,m):
        method = Method.MethodWindow(self,m)
        method.grab_set()

    def on_standard(self):
        if self.list_window is None:
            self.list_window = List.ListWindow(self)
        else:
            self.list_window.destroy()
            self.list_window = None

    def on_calibrate(self):
        self.run("S.calibrate()")
        if self.calibration_window is None:
            self.calibration_window = Calibration.CalibrationWindow(self)
        else:
            self.calibration_window.refresh()

    def on_export(self):
        self.run("S.TODO()")

    def on_view(self):
        if self.view_window is None and len(S.get('samples'))>0:
            self.view_window = View.ViewWindow(self)
        else:
            self.view_window.destroy()
            self.view_window = None

    def toggle_log_window(self):
        if self.log_window is None:
            self.log_window = Log.LogWindow(self)
            self.log_window.show()
        else:
            self.log_window.destroy()
            self.log_window = None

    def on_template(self):
        self.run("S.TODO()")

    def on_settings(self):
        self.run("S.TODO()")

    def on_help(self):
        if self.help_window is None:
            self.help_window = Doc.HelpWindow(self,item='top')
        else:
            self.help_window.destroy()
            self.help_window = None

def offset(parent,child):
    x_offset = parent.winfo_x()
    width = parent.winfo_width()
    y_offset = parent.winfo_y()
    child.geometry("+{}+{}".format(x_offset+width, y_offset))
