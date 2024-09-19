import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
from . import Main
from ..API import Refmats

class ListWindow(tk.Toplevel):

    def __init__(self,top):
        super().__init__(top)
        self.title('Select standards')
        Main.offset(top,self)
        row = 0
        samples = S.get('samples')
        if len(samples)>10: self.geometry('400x600')
        selections = dict.fromkeys(samples.index,None)
        for key, sample in samples.items():
            label = ttk.Label(self,text=key)
            label.grid(row=row,column=0,padx=1,pady=1)
            selections[key] = tk.StringVar()
            method = S.get('method').name
            refmats = Refmats.get_names(method)
            combo = ttk.Combobox(self,values=refmats,textvariable=selections[key])
            combo.set(sample.group)
            combo.grid(row=row,column=1,padx=1,pady=1)
            row += 1
        button = ttk.Button(self,text='Save',
                            command=lambda t=top,s=selections: self.on_click(t,s))
        button.grid(row=row,columnspan=2)

    def on_click(self,top,selections):
        groups = dict()
        i = 0
        for key in selections:
            group = selections[key].get()
            if group == 'sample':
                pass
            elif group in groups:
                groups[group].append(i)
            else:
                groups[group] = [i]
            i += 1
        blocks = []
        for group, indices in groups.items():
            blocks.append(group + "=[" + ",".join(map(str,indices)) + "]")
        cmd = "S.standards(" + ",".join(blocks) + ")"
        top.run(cmd)

            
