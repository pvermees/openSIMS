import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
from . import Main

class OpenWindow(tk.Toplevel):

    def __init__(self,top):
        super().__init__(top)
        self.title('Choose an instrument')
        Main.offset(top,self)
        self.create_Cameca_button(top)
        self.create_SHRIMP_button(top)

    def create_Cameca_button(self,top):
        button = ttk.Button(self,text='Cameca',
                            command=lambda t=top: self.on_Cameca(t))
        button.pack(expand=True,fill=tk.BOTH)

    def create_SHRIMP_button(self,top):
        button = ttk.Button(self,text='SHRIMP',
                            command=lambda t=top: self.on_SHRIMP(t))
        button.pack(expand=True,fill=tk.BOTH)

    def on_Cameca(self,top):
        path = fd.askdirectory()
        self.read(top,path,'Cameca')

    def on_SHRIMP(self,top):
        path = fd.askopenfile()
        self.read(top,path,'SHRIMP')

    def read(self,top,path,instrument):
        top.run("S.set('instrument','{i}')".format(i=instrument))
        top.run("S.set('path','{p}')".format(p=path))
        top.run("S.read()")
        top.open_window = None
        self.destroy()
