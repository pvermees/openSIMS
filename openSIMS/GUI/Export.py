import importlib
import traceback
import openSIMS as S
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
from . import Main, Doc

class ExportWindow(tk.Toplevel):

    def __init__(self,top,button):
        super().__init__(top)
        self.title('Export')
        Main.offset(button,self)
        self.top = top
        self.help_window = None
        self.create_combo_box()
        self.create_OK_button()
        self.create_Help_button()

    def create_combo_box(self):
        label = ttk.Label(self,text='Choose a format:')
        label.pack(side=tk.TOP,fill=tk.X,pady=2)
        self.exporters = S.simplex().exporters()
        self.var = tk.StringVar()
        combo = ttk.Combobox(self,values=self.exporters,textvariable=self.var)
        self.var.set(self.top.exporter)
        combo.pack(side=tk.TOP,fill=tk.X,pady=2)
        
    def create_OK_button(self):
        OK = ttk.Button(self,text='OK')
        OK.bind("<Button-1>",self.on_export)
        OK.pack(side=tk.LEFT,fill=tk.X,pady=2)

    def create_Help_button(self):        
        HELP = ttk.Button(self,text='HELP')
        HELP.bind("<Button-1>",self.on_help)
        HELP.pack(side=tk.LEFT,fill=tk.X,pady=2)
        
    def on_export(self,event):
        fmt = self.var.get()
        path = fd.asksaveasfile(mode='w')
        try:
            S.export_csv(path,fmt=fmt)
        except ValueError as e:
            tk.messagebox.showwarning(message=e)
        self.top.exporter = fmt
        self.top.export_window = None
        self.destroy()

    def on_help(self,event):
        fmt = self.var.get()
        module_name = 'openSIMS.Methods.Exporters.' + fmt
        module = importlib.import_module(module_name)
        msg = module.help()
        if self.help_window is None:
            self.help_window = Doc.HelpWindow(self,event.widget,text=msg)
        else:
            self.help_window.destroy()
            self.help_window = None
