import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
from . import Main, Doc

class OpenWindow(tk.Toplevel):

    def __init__(self,top,button):
        super().__init__(top)
        self.title('Choose an instrument')
        self.help_window = None
        Main.offset(button,self)
        self.create_Cameca_button()
        self.create_SHRIMP_button()
        self.create_Help_button()
        self.protocol("WM_DELETE_WINDOW",self.on_closing)

    def on_closing(self):
        setattr(self.master,'open_window',None)
        self.destroy()

    def create_Cameca_button(self):
        button = ttk.Button(self,text='Cameca')
        button.bind("<Button-1>",self.on_Cameca)
        button.pack(expand=True,fill=tk.BOTH)

    def create_SHRIMP_button(self):
        button = ttk.Button(self,text='SHRIMP')
        button.bind("<Button-1>",self.on_SHRIMP)
        button.pack(expand=True,fill=tk.BOTH)

    def create_Help_button(self):
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
        self.master.run("S.set('instrument','{i}')".format(i=instrument))
        self.master.run("S.set('path','{p}')".format(p=path))
        self.master.run("S.read()")
        self.master.open_window = None
        self.destroy()
