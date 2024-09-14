import openSIMS as S
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.ttk as ttk
import tkinter.scrolledtext as st
import tkinter.font as font
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

class gui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('openSIMS')
        self.figs = [111]
        self.log_window = None
        self.help_window = None
        self.create_open_button()
        self.create_method_button()
        self.create_standard_button()
        self.create_process_button()
        self.create_export_button()
        self.create_plot_button()
        self.create_list_button()
        self.create_log_button()
        self.create_template_button()
        self.create_settings_button()
        self.create_help_button()

    def run(self,cmd):
        S.get('stack').append(cmd)
        exec(cmd)
        if self.log_window is not None:
            self.log_window.log(cmd=cmd)

    def create_open_button(self):
        button = ttk.Menubutton(self,text='Open',direction="right")
        menu = tk.Menu(button, tearoff=0)
        menu.add_command(label="Cameca",
                         command=lambda inst="Cameca": self.on_open(inst))
        menu.add_command(label="SHRIMP",
                         command=lambda inst="SHRIMP": self.on_open(inst))
        button["menu"] = menu
        button.pack(expand=True)

    def create_method_button(self):
        button = ttk.Button(self,text='Method',command=self.on_method)
        button.pack(expand=True)

    def create_standard_button(self):
        button = ttk.Button(self,text='Standards',command=self.set_standard)
        button.pack(expand=True)

    def create_process_button(self):
        button = ttk.Button(self,text='Process',command=self.on_process)
        button.pack(expand=True)

    def create_export_button(self):
        button = ttk.Button(self,text='Export',command=self.on_export)
        button.pack(expand=True)

    def create_plot_button(self):
        button = ttk.Button(self,text='Plot',command=self.on_plot)
        button.pack(expand=True)

    def create_list_button(self):
        button = ttk.Button(self,text='List',command=self.on_list)
        button.pack(expand=True)

    def create_log_button(self):
        button = ttk.Button(self,text='Log',command=self.toggle_log_window)
        button.pack(expand=True)

    def create_template_button(self):
        button = ttk.Button(self,text='Template',command=self.on_template)
        button.pack(expand=True)

    def create_settings_button(self):
        button = ttk.Button(self,text='Settings',command=self.on_settings)
        button.pack(expand=True)

    def create_help_button(self):
        button = ttk.Button(self,text='Help',command=self.on_help)
        button.pack(expand=True)

    def on_open(self,instrument):
        self.run("S.set('instrument','{i}')".format(i=instrument))
        path = fd.askdirectory() if instrument=='Cameca' else fd.askopenfile()
        self.run("S.set('path','{p}')".format(p=path))
        self.run("S.read()")

    def on_method(self):
        method = MethodWindow(self)
        method.grab_set()

    def set_standard(self):
        self.run("S.TODO()")

    def on_process(self):
        self.run("S.TODO()")

    def on_export(self):
        self.run("S.TODO()")

    def on_plot(self):
        if len(S.get('samples'))>0:
            plot_window = PlotWindow(self)

    def on_list(self):
        self.run("S.TODO()")

    def toggle_log_window(self):
        if self.log_window is None:
            self.log_window = LogWindow(self)
            self.log_window.show()
        else:
            self.log_window.destroy()
            self.log_window = None

    def on_template(self):
        self.run("S.TODO()")

    def on_settings(self):
        self.run("S.TODO()")

    def on_help(self):
        if self.help_window is None:
            self.help_window = HelpWindow(self,item='top')
        else:
            self.help_window.destroy()
            self.help_window = None

class MethodWindow(tk.Toplevel):

    def __init__(self,top):
        super().__init__(top)
        self.title('Method')
        self.create_test_button(top)
        offset(top,self)

    def create_test_button(self,top):
        button = ttk.Button(self,text='Test',
                            command=lambda t=top: self.on_test(t))
        button.pack(expand=True)

    def on_test(self,top):
        top.run("S.TODO()")
        self.destroy()

class HelpWindow(tk.Toplevel):

    def __init__(self,top,item='top'):
        super().__init__(top)
        self.title('Help')
        offset(top,self)
        from openSIMS import doc
        label = tk.Label(self,text=doc.Help(item),anchor='w',justify='left')
        label.bind('<Configure>', lambda e: label.config(wraplength=label.winfo_width()))
        label.pack(expand=True,fill=tk.BOTH)

class LogWindow(tk.Toplevel):

    def __init__(self,top):
        super().__init__(top)
        self.title('log')
        offset(top,self)
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

class PlotWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__()
        self.title('Plot')
        offset(top,self)
        fig, axs = S.plot(show=False,num=top.figs[0])
  
        canvas = FigureCanvasTkAgg(fig,master=self)
        canvas.get_tk_widget().pack(expand=tk.TRUE,fill=tk.BOTH)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
  
        previous_button = ttk.Button(self,text='<',
                                     command=lambda c=canvas,t=top:
                                     self.plot_previous(t,c))
        previous_button.pack(expand=tk.TRUE,side=tk.LEFT)
        next_button = ttk.Button(self,text='>',
                                 command=lambda c=canvas,t=top:
                                 self.plot_next(t,c))
        next_button.pack(expand=tk.TRUE,side=tk.LEFT)

    def plot_previous(self,top,canvas):
        self.refresh_canvas(top,canvas,-1)

    def plot_next(self,top,canvas):
        self.refresh_canvas(top,canvas,+1)

    def refresh_canvas(self,top,canvas,di):
        ns = len(S.get('samples'))
        i = (S.get('i') + di) % ns
        S.set('i',i)
        canvas.figure.clf()
        canvas.figure, axs = S.plot(show=False,num=top.figs[0])
        canvas.draw()
        
def offset(parent,child):
    x_offset = parent.winfo_x()
    width = parent.winfo_width()
    y_offset = parent.winfo_y()
    child.geometry("+{}+{}".format(x_offset+width, y_offset))
