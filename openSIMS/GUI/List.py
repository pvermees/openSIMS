import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
from . import Main

class ListWindow(tk.Toplevel):

    refmats = ['sample','Plesovice','GJ1']

    def __init__(self,top):
        super().__init__(top)
        self.title('Select standards')
        Main.offset(top,self)
        row = 0
        samples = S.get('samples')
        if len(samples)>10: self.geometry('400x600')
        for key, sample in samples.items():
            label = ttk.Label(self,text=key)
            label.grid(row=row,column=0,padx=1,pady=1)
            combo = ttk.Combobox(self,values=self.refmats)
            combo.set(sample.group)
            combo.grid(row=row,column=1,padx=1,pady=1)
            row += 1
        button = ttk.Button(self,text='Set',
                            command=lambda t=top: self.on_click(t))
        button.grid(row=row,columnspan=2)

    def on_click(self,top):
        top.run('S.TODO()')
