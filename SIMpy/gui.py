import tkinter as tk
import tkinter.filedialog as fd
from tkinter import ttk

class MethodWindow(tk.Toplevel):
    
    def __init__(self,parent):
        super().__init__(parent)
        self.title('method')
        
        ttk.Button(self,text='Close',command=self.destroy).pack()

class gui(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title('SIMpy')
        ttk.Button(self,text='Open',command=self.on_open).pack()
        ttk.Button(self,text='Method',command=self.on_method).pack()
        ttk.Button(self,text='Exit',command=self.destroy).pack()

    def on_open(self):
        fd.askdirectory()

    def on_method(self):
        method = MethodWindow(self)
        method.grab_set()

if __name__ == "__main__":
    app = gui()
    app.mainloop()
