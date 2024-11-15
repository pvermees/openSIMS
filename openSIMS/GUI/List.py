import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import os.path
from . import Main

class ListWindow(tk.Toplevel):

    def __init__(self,top,button):
        super().__init__(top)
        self.title('Select standards')

        samples = S.get('samples')
        refmats = ['sample'] + self.shared_refmats()
        self.combo_labels = []
        self.combo_vars = []
        self.combo_boxes = []
        Main.offset(button,self)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self,orient="vertical",command=canvas.yview)
        frame = ttk.Frame(canvas)
        frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0,0),window=frame,anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        row = 0
        for sname, sample in samples.items():
            label = ttk.Label(frame,text=sname)
            label.grid(row=row,column=0,padx=1,pady=1)
            var = tk.StringVar()
            combo = ttk.Combobox(frame,values=refmats,textvariable=var)
            combo.set(sample.group)
            combo.grid(row=row,column=1,padx=1,pady=1)
            combo.bind("<<ComboboxSelected>>",self.on_change)
            self.combo_labels.append(label)
            self.combo_vars.append(var)
            self.combo_boxes.append(combo)
            row += 1
        canvas.grid(row=0,column=0,columnspan=2)
        scrollbar.grid(row=0,column=2,sticky='ns')
        save = ttk.Button(self,text='Save',command=self.on_save)
        reset = ttk.Button(self,text='Reset',command=self.on_reset)
        save.grid(row=1,column=0)
        reset.grid(row=1,column=1)
        self.protocol("WM_DELETE_WINDOW",self.on_closing)

    def on_closing(self):
        setattr(self.master,'standard_window',None)
        self.destroy()

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

    def shared_refmats(self):
        method_list = S.list_methods()
        refmats = set(S.settings(method_list[0])['refmats'].index)
        for method in method_list:
            refmats = refmats & set(S.settings(method)['refmats'].index)
        return list(refmats)

    def on_save(self):
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
        self.master.run(cmd)

    def on_reset(self):
        for combo in self.combo_boxes:
            combo.set('sample')
