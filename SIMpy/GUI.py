import tkinter as tk
import tkinter.filedialog as fd
import tkinter.ttk as ttk

class gui(tk.Tk):

    def __init__(self,settings):
        super().__init__()
        self.title('SIMpy')
        self.SP = settings
        ttk.Button(self,text='Open',command=self.on_open).pack()
        ttk.Button(self,text='Method',command=self.on_method).pack()
        ttk.Button(self,text='Exit',command=self.destroy).pack()

    def on_open(top):
        top.SP.datadir = fd.askdirectory()

    def on_method(top):
        method = MethodWindow(top)
        method.grab_set()

class MethodWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__(top)
        self.title('method')
        print(top.SP.datadir)
        ttk.Button(self,text='Close',command=self.destroy).pack()
