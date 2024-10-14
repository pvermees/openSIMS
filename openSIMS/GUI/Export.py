import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from . import Main

class ExportWindow(tk.Toplevel):

    def __init__(self,top,button):
        super().__init__(top)
        self.title('Export')
        Main.offset(button,self)
        label = ttk.Label(self,text='Choose a format:')
        label.pack(side=tk.TOP,fill=tk.X,pady=2)
        exporters = S.simplex().exporters()
        self.var = tk.StringVar()
        combo = ttk.Combobox(self,values=exporters,textvariable=self.var)
        self.var.set('default')
        combo.pack(side=tk.TOP,fill=tk.X,pady=2)
        OK = ttk.Button(self,text='OK')
        OK.pack(side=tk.LEFT,anchor=tk.SW,pady=2)
        HELP = ttk.Button(self,text='HELP')
        HELP.pack(side=tk.LEFT,anchor=tk.SE,pady=2)
