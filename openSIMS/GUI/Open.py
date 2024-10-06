import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
from . import Main

class OpenWindow(tk.Toplevel):

    def __init__(self,top,button):
        super().__init__(top)
        self.top = top
        self.title('Choose an instrument')
        Main.offset(button,self)
        self.create_Cameca_button(top)
        self.create_SHRIMP_button(top)

    def create_Cameca_button(self,top):
        button = ttk.Button(self,text='Cameca')
        button.bind("<Button-1>",self.on_Cameca)
        button.pack(expand=True,fill=tk.BOTH)

    def create_SHRIMP_button(self,top):
        button = ttk.Button(self,text='SHRIMP')
        button.bind("<Button-1>",self.on_SHRIMP)
        button.pack(expand=True,fill=tk.BOTH)

    def on_Cameca(self,event):
        path = fd.askdirectory()
        self.read(path,'Cameca')

    def on_SHRIMP(self,event):
        path = fd.askopenfile()
        self.read(path,'SHRIMP')

    def read(self,path,instrument):
        self.top.run("S.set('instrument','{i}')".format(i=instrument))
        self.top.run("S.set('path','{p}')".format(p=path))
        self.top.run("S.read()")
        self.top.open_window = None
        self.destroy()
