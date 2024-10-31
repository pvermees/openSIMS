import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from . import Main
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ViewWindow(tk.Toplevel):
    
    def __init__(self,top,button):
        super().__init__(top)
        self.top = top
        self.title('View')
        Main.offset(button,self)

        fig = plt.figure(top.figures['view'])
        canvas = FigureCanvasTkAgg(fig,master=self)
        canvas.figure, axs = S.view()
        canvas.get_tk_widget().pack(expand=tk.TRUE,fill=tk.BOTH)
        canvas.draw()
  
        previous_button = ttk.Button(self,text='<',
                                     command=lambda c=canvas:
                                     self.view_previous(c))
        previous_button.pack(expand=tk.TRUE,side=tk.LEFT)
        next_button = ttk.Button(self,text='>',
                                 command=lambda c=canvas:
                                 self.view_next(c))
        next_button.pack(expand=tk.TRUE,side=tk.LEFT)
        self.protocol("WM_DELETE_WINDOW",self.on_closing)

    def on_closing(self):
        setattr(self.top,'view_window',None)
        self.destroy()

    def view_previous(self,canvas):
        self.refresh_canvas(canvas,-1)

    def view_next(self,canvas):
        self.refresh_canvas(canvas,+1)

    def refresh_canvas(self,canvas,di):
        ns = len(S.get('samples'))
        i = (S.get('i') + di) % ns
        S.set('i',i)
        canvas.figure.clf()
        canvas.figure, axs = S.view()
        canvas.draw()
