import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
from . import Main
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ViewWindow(tk.Toplevel):
    
    def __init__(self,top,button):
        super().__init__(top)
        self.title('View')
        Main.offset(button,self)

        fig, self.ax = S.view()        
        
        self.canvas = FigureCanvasTkAgg(fig,master=self)
        self.canvas.get_tk_widget().pack(expand=tk.TRUE,fill=tk.BOTH)
        self.canvas.draw()
  
        previous_button = ttk.Button(self,text='<',command=self.view_previous)
        previous_button.pack(expand=tk.TRUE,side=tk.LEFT)
        next_button = ttk.Button(self,text='>',command=self.view_next)
        next_button.pack(expand=tk.TRUE,side=tk.LEFT)
        self.protocol("WM_DELETE_WINDOW",self.on_closing)

    def on_closing(self):
        setattr(self.master,'view_window',None)
        self.destroy()

    def view_previous(self):
        self.refresh_canvas(-1)

    def view_next(self):
        self.refresh_canvas(+1)

    def refresh_canvas(self,di):
        ns = len(S.get('samples'))
        i = (S.get('i') + di) % ns
        S.set('i',i)
        self.canvas.figure.clf()
        self.canvas.figure, axs = S.view()
        self.canvas.draw()
