import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
from . import Main

class MethodWindow(tk.Toplevel):

    def __init__(self,top,m):
        super().__init__(top)
        self.title('Pair the ions with the channels')
        Main.offset(top,self)
        refresh = (m != S.get('method'))
        oldselections = None if refresh else S.get('channels')
        ions = S.settings(m)['ions']
        channels = S.simplex().all_channels()
        newselections = dict.fromkeys(ions,None)
        row = 0
        for ion in ions:
            label = ttk.Label(self,text=ion)
            label.grid(row=row,column=0,padx=1,pady=1)
            newselections[ion] = tk.StringVar()
            combo = ttk.Combobox(self,values=channels,textvariable=newselections[ion])
            default = self.guess(ion,channels) if refresh else oldselections[ion]
            combo.set(default)
            combo.grid(row=row,column=1,padx=1,pady=1)
            row += 1
        button = ttk.Button(self,text='OK',
                            command=lambda t=top,m=m,s=newselections: self.on_click(t,m,s))
        button.grid(row=row,columnspan=2)

    def guess(self,ion,channels):
        bestoverlap = 0
        out = channels[0]
        for channel in channels:
            newoverlap = len(set(ion).intersection(channel))
            if newoverlap > bestoverlap:
                bestoverlap = newoverlap
                out = channel
        return out

    def on_click(self,top,m,selections):
        cmd = "S.method('{m}'".format(m=m)
        for key in selections:
            val = selections[key].get()
            cmd += "," + key + "='" + val + "'"
        cmd += ")"
        top.run(cmd)
        self.destroy()
