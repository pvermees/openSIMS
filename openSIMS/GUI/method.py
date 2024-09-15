import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
from . import main

class MethodWindow(tk.Toplevel):

    def __init__(self,top,meth):
        super().__init__(top)
        self.title('Method')
        self.create_test_button(top)
        main.offset(top,self)
        print(S.channels())

    def create_test_button(self,top):
        button = ttk.Button(self,text='Test',
                            command=lambda t=top: self.on_test(t))
        button.pack(expand=True)

    def on_test(self,top):
        top.run("S.TODO()")
        self.destroy()
