import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
from . import Main
from ..API import Method

class MethodWindow(tk.Toplevel):

    def __init__(self,top,m):
        super().__init__(top)
        self.title('Pair the ions with the channels')
        Main.offset(top,self)
        channels = S.get('channels')
        row = 0
        for ion in Method.method2ions(m):
            label = ttk.Label(self,text=ion)
            label.grid(row=row,column=0,padx=2,pady=2)
            combo = ttk.Combobox(self,values=channels)
            combo.set("Pick a channel")
            combo.grid(row=row,column=1,padx=2,pady=2)
            row += 1
        button = ttk.Button(self,text='OK',command=lambda t=top: self.on_click(t))
        button.grid(row=row,columnspan=2)

    def on_click(self,top):
        top.run('S.TODO()')
        self.destroy()
