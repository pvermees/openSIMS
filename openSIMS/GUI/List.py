import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
from . import Main
from ..API import Refmats

class ListWindow(tk.Toplevel):

    def __init__(self,top):
        super().__init__(top)
        self.title('Select standards')
        samples = S.get('samples')
        snames = list(samples.keys())
        self.combo_labels = []
        self.combo_vars = []
        self.combo_boxes = []
        Main.offset(top,self)
        if len(samples)>20: self.geometry('400x600')
        method = S.get('method').name
        refmats = ['sample'] + Refmats.get_names(method)
        row = 0
        for sname, sample in samples.items():
            label = ttk.Label(self,text=sname)
            label.grid(row=row,column=0,padx=1,pady=1)
            var = tk.StringVar()
            combo = ttk.Combobox(self,values=refmats,textvariable=var)
            combo.set(sample.group)
            combo.grid(row=row,column=1,padx=1,pady=1)
            combo.bind("<<ComboboxSelected>>",self.on_change)
            self.combo_labels.append(label)
            self.combo_vars.append(var)
            self.combo_boxes.append(combo)
            row += 1
        button = ttk.Button(self,text='Save',
                            command=lambda t=top: self.on_click(t))
        button.grid(row=row,columnspan=2)

    def on_change(self,event):
        groups = self.all_groups()
        prefixes = set(S.get('prefixes').keys())
        i = self.combo_boxes.index(event.widget)
        sname = self.combo_labels[i].cget('text')
        group = event.widget.get()
        ignore = S.get('ignore')
        if group == 'sample':
            ignore.add(sname)
        elif sname in ignore:
            ignore.remove(sname)
        else:
            pass
        removed = prefixes.difference(groups)

    def all_groups(self):
        out = set()
        for i, box in enumerate(self.combo_boxes):
            out.add(box.get())
        return out

    def on_click(self,top):
        groups = dict()
        for i, var in enumerate(self.combo_vars):
            group = var.get()
            if group == 'sample':
                pass
            elif group in groups:
                groups[group].append(i)
            else:
                groups[group] = [i]
        blocks = []
        for group, indices in groups.items():
            blocks.append(group + "=[" + ",".join(map(str,indices)) + "]")
        cmd = "S.standards(" + ",".join(blocks) + ")"
        top.run(cmd)


def intersect(s1, s2):
    m = len(s1)
    n = len(s2)
    res = 0
    for i in range(m):
        for j in range(n):
            curr = 0
            while (i + curr) < m and (j + curr) < n and s1[i + curr] == s2[j + curr]:
                curr += 1
            res = max(res, curr)
    return res
    
