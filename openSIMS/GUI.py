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

    def __init__(self,settings):
        super().__init__()
        self.title('openSIMS')
        self.sp = settings
        self.figs = [111]
        self.stack = []
        self.header = ["import openSIMS",
                       "sp = openSIMS.simplex(gui=True)"]
        self.log_window = None
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

    def log(self,cmd):
        self.stack.append(cmd)
        exec('self.' + cmd)
        if self.log_window is not None:
            self.log_window.refresh(self)

    def run(self):
        self.sp.reset()
        for cmd in self.stack:
            exec('self.' + cmd)

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
        self.log("sp.set_instrument('{i}')".format(i=instrument))
        path = fd.askdirectory() if instrument=='Cameca' else fd.askopenfile()
        self.log("sp.set_path('{p}')".format(p=path))
        self.log("sp.read()")

    def on_method(self):
        method = MethodWindow(self)
        method.grab_set()
        
    def set_standard(self):
        self.log("sp.TODO()")

    def on_process(self):
        self.log("sp.TODO()")

    def on_export(self):
        self.log("sp.TODO()")

    def on_plot(self):
        if len(self.sp.samples)>0:
            plot_window = PlotWindow(self)
        
    def on_list(self):
        self.log("sp.TODO()")
        
    def toggle_log_window(self):
        if self.log_window is None:
            self.log_window = LogWindow(self)
            self.log_window.refresh(self)
        else:
            self.log_window.destroy()
            self.log_window = None

    def on_template(self):
        self.log("sp.TODO()")
        
    def on_settings(self):
        self.log("sp.TODO()")

    def on_help(self):
        self.log("sp.TODO()")
        
class MethodWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__(top)
        self.title('method')
        self.create_test_button(top)
        offset(top,self)

    def create_test_button(self,top):
        button = ttk.Button(self,text='Test',
                            command=lambda t=top: self.on_test(t))
        button.pack(expand=True)

    def on_test(self,top):
        top.log("sp.TODO()")
        self.destroy()

class LogWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__(top)
        self.title('log')
        offset(top,self)
        self.protocol('WM_DELETE_WINDOW',top.toggle_log_window)
        self.script = st.ScrolledText(self)
        self.script.pack(side=tk.BOTTOM,expand=True,fill=tk.BOTH)
        open_button = ttk.Button(self,text='Open',
                                 command=lambda t=top: self.load(t))
        open_button.pack(expand=True,side=tk.LEFT)
        save_button = ttk.Button(self,text='Save',
                                 command=lambda t=top: self.save(t))
        save_button.pack(expand=True,side=tk.LEFT)
        run_button = ttk.Button(self,text='Run',command=top.run)
        run_button.pack(expand=True,side=tk.LEFT)
        clear_button = ttk.Button(self,text='Clear',
                                  command=lambda t=top: self.clear(t))
        clear_button.pack(expand=True,side=tk.LEFT)

    def refresh(self,top):
        self.script.config(state=tk.NORMAL)
        self.script.delete(1.0,tk.END)
        self.script.insert(tk.INSERT,'\n'.join(top.header))
        self.script.insert(tk.INSERT,'\n')
        self.script.insert(tk.INSERT,'\n'.join(top.stack))
        self.script.config(state=tk.DISABLED)
        
    def load(self,top):
        file = fd.askopenfile()
        top.stack = file.read().splitlines()[len(top.header):]
        self.refresh(top)
        file.close()

    def save(self,top):
        file = fd.asksaveasfile(mode='w')
        file.writelines('\n'.join(top.header))
        file.writelines('\n'.join(top.stack))
        file.close()

    def clear(self,top):
        top.stack = []
        self.script.config(state=tk.NORMAL)
        self.script.delete(1.0,tk.END)
        self.script.insert(tk.INSERT,'\n'.join(top.header))
        self.script.config(state=tk.DISABLED)

class PlotWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__()
        self.title('Plot')
        offset(top,self)
        fig, axs = top.sp.plot(show=False,num=top.figs[0])
  
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
        refresh_canvas(self,top,canvas,-1)

    def plot_next(self,top,canvas):
        refresh_canvas(self,top,canvas,+1)

def refresh_canvas(self,top,canvas,di):
    ns = len(top.sp.samples)
    top.sp.i = (top.sp.i + di) % ns
    canvas.figure.clf()
    canvas.figure, axs = top.sp.plot(show=False,num=top.figs[0])
    canvas.draw()
        
def offset(parent,child):
    x_offset = parent.winfo_x()
    width = parent.winfo_width()
    y_offset = parent.winfo_y()
    child.geometry("+{}+{}".format(x_offset+width, y_offset))
