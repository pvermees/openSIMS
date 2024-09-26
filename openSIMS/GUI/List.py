import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import os.path
from . import Main
from ..API import Settings

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
        method = S.get('method')
        refmats = ['sample'] + list(S.settings(method)['refmats'].index)
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
        i = self.combo_boxes.index(event.widget)
        changed = self.combo_labels[i].cget('text')
        ignored = S.get('ignore')
        if event.widget.get() == 'sample':
            ignored.add(changed)
        elif changed in ignored:
            ignored.remove(changed)
        else:
            pass
        prefixes = self.get_prefixes()
        self.set_prefixes(prefixes)

    def get_prefixes(self):
        groups = self.all_groups()
        prefixes = dict.fromkeys(groups,None)
        ignored = S.get('ignore')
        for i, box in enumerate(self.combo_boxes):
            sname = self.combo_labels[i].cget('text')
            group = box.get()
            if sname not in ignored and group != 'sample':
                if prefixes[group] is None:
                    prefixes[group] = sname
                else:
                    prefixes[group] = os.path.commonprefix([sname,prefixes[group]])
        return prefixes

    def set_prefixes(self,prefixes):
        ignored = S.get('ignore')
        for i, box in enumerate(self.combo_boxes):
            sname = self.combo_labels[i].cget('text')
            if sname not in ignored:
                group = self.match_prefix(sname,prefixes)
                box.set(group)

    def match_prefix(self,sname,prefixes):
        for group, prefix in prefixes.items():
            if sname.startswith(prefix):
                return group
        return 'sample'

    def all_groups(self):
        out = set()
        for i, box in enumerate(self.combo_boxes):
            group = box.get()
            if group != 'sample':
                out.add(group)
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
