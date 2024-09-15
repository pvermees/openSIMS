import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.scrolledtext as st
from . import Main

class LogWindow(tk.Toplevel):

    def __init__(self,top):
        super().__init__(top)
        self.title('log')
        Main.offset(top,self)
        self.protocol('WM_DELETE_WINDOW',top.toggle_log_window)
        self.script = st.ScrolledText(self)
        self.script.pack(side=tk.BOTTOM,expand=True,fill=tk.BOTH)
        open_button = ttk.Button(self,text='Open',command=self.load)
        open_button.pack(expand=True,side=tk.LEFT)
        save_button = ttk.Button(self,text='Save',command=self.save)
        save_button.pack(expand=True,side=tk.LEFT)
        clear_button = ttk.Button(self,text='Clear',command=self.clear)
        clear_button.pack(expand=True,side=tk.LEFT)

    def show(self,run=False):
        for cmd in S.get('stack'):
            self.log(cmd=cmd)
            if run: exec(cmd)

    def log(self,cmd=None):
        self.script.config(state=tk.NORMAL)
        if cmd is None:
            self.script.delete(1.0,tk.END)
        else:
            self.script.insert(tk.INSERT,cmd)
            self.script.insert(tk.INSERT,'\n')
        self.script.config(state=tk.DISABLED)
        
    def load(self):
        file = fd.askopenfile()
        stack = file.read().splitlines()
        file.close()
        S.set('stack',stack)
        self.run()

    def run(self):
        S.reset()
        self.log()
        self.show(run=True)

    def save(self):
        file = fd.asksaveasfile(mode='w')
        file.writelines('\n'.join(S.get('stack')))
        file.close()

    def clear(self):
        header = S.get('header')
        S.set('stack',[header])
        self.log()
        self.log(cmd=header)
