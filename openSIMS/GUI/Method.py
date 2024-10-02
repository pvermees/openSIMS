import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from . import Main

class MethodWindow(tk.Toplevel):

    def __init__(self,top):
        super().__init__(top)
        self.title('Choose methods')
        Main.offset(top,self)
        self.variables = self.create_vars()
        for method, variable in self.variables.items():
            check = tk.Checkbutton(self,text=method,variable=variable,
                                   command = lambda t=top,m=method:
                                   self.set_channels(t,m))
            check.pack(anchor='w')

    def sorted_methods(self):
        methods = np.array([])
        types = np.array([])
        for method, settings in S.settings().items():
            types = np.append(types,settings['type'])
            methods = np.append(methods,method)
        order = np.argsort(types)
        return methods[order]

    def create_vars(self):
        all_methods = self.sorted_methods()
        variables = dict()
        for method in all_methods:
            checked = method in S.get('methods').keys()
            variables[method] = tk.IntVar(value=checked)
        return variables

    def set_channels(self,top,method):
        if self.variables[method].get():
            win = ChannelWindow(top,method)
        else:
            cmd = "S.remove_method('{m}')".format(m=method)
            top.run(cmd)
    
class ChannelWindow(tk.Toplevel):

    def __init__(self,top,m):
        super().__init__(top)
        self.title('Pair the ions with the channels')
        Main.offset(top,self)
        methods = S.get('methods')
        refresh = (m not in methods.keys())
        oldselections = None if refresh else methods[m]
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
        cmd = "S.add_method('{m}'".format(m=m)
        for key in selections:
            val = selections[key].get()
            cmd += "," + key + "='" + val + "'"
        cmd += ")"
        top.run(cmd)
        self.destroy()
