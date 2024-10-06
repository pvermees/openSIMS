import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
from . import Main, Doc

class OpenWindow(tk.Toplevel):

    def __init__(self,top,button):
        super().__init__(top)
        self.top = top
        self.title('Choose an instrument')
        self.help_window = None
        Main.offset(button,self)
        self.create_Cameca_button(top)
        self.create_SHRIMP_button(top)
        self.create_Help_button(top)

    def create_Cameca_button(self,top):
        button = ttk.Button(self,text='Cameca')
        button.bind("<Button-1>",self.on_Cameca)
        button.pack(expand=True,fill=tk.BOTH)

    def create_SHRIMP_button(self,top):
        button = ttk.Button(self,text='SHRIMP')
        button.bind("<Button-1>",self.on_SHRIMP)
        button.pack(expand=True,fill=tk.BOTH)

    def create_Help_button(self,top):
        button = ttk.Button(self,text='Help')
        button.bind("<Button-1>",self.on_Help)
        button.pack(expand=True,fill=tk.BOTH)

    def on_Cameca(self,event):
        path = fd.askdirectory()
        self.read(path,'Cameca')

    def on_SHRIMP(self,event):
        path = fd.askopenfile()
        self.read(path,'SHRIMP')
        
    def on_Help(self,event):
        if self.help_window is None:
            self.help_window = Doc.HelpWindow(self,event.widget,item='open')
        else:
            self.help_window.destroy()
            self.help_window = None
        
    def read(self,path,instrument):
        self.top.run("S.set('instrument','{i}')".format(i=instrument))
        self.top.run("S.set('path','{p}')".format(p=path))
        self.top.run("S.read()")
        self.top.open_window = None
        self.destroy()
