import tkinter as tk
import tkinter.filedialog as fd
import tkinter.ttk as ttk
import tkinter.scrolledtext as st

class gui(tk.Tk):

    def __init__(self,settings):
        super().__init__()
        self.title('SIMpy')
        self.sp = settings
        self.stack = ["from SIMpy import SIMpy",
                      "sp = SIMpy(gui=True)"]
        self.log = None
        self.create_open_button()
        self.create_method_button()
        self.create_log_button()
        self.create_exit_button()

    def run(self,cmd):
        self.stack.append(cmd)
        exec('self.' + cmd)
        if self.log is not None:
            self.log.refresh(self.stack)

    def create_open_button(self):
        button = ttk.Menubutton(self,text='Open',direction="right")
        menu = tk.Menu(button, tearoff=0)
        menu.add_command(label="SHRIMP",
                         command=lambda inst="SHRIMP": self.on_open(inst))
        menu.add_command(label="Cameca",
                         command=lambda inst="Cameca": self.on_open(inst))
        button["menu"] = menu
        button.pack(expand=True)
        
    def create_method_button(self):
        button = ttk.Button(self,text='Method',command=self.on_method)
        button.pack(expand=True)

    def create_log_button(self):
        button = ttk.Button(self,text='Log',command=self.toggle_log)
        button.pack(expand=True)

    def create_exit_button(self):
        button = ttk.Button(self,text='Exit',command=self.destroy)
        button.pack(expand=True)

    def on_open(top,instrument):
        data_dir = fd.askdirectory()
        top.run("sp.set_instrument('{i}')".format(i=instrument))
        top.run("sp.set_data_dir('{d}')".format(d=data_dir))

    def on_method(top):
        method = MethodWindow(top)
        method.grab_set()

    def toggle_log(top):
        if top.log is None:
            top.log = LogWindow(top)
            top.log.refresh(top.stack)
        else:
            top.log.destroy()
            top.log = None
        
class MethodWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__(top)
        self.title('method')
        ttk.Button(self,text='Close',command=self.destroy).pack()

class LogWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__(top)
        self.title('log')
        self.script = st.ScrolledText(self)
        self.script.pack(side=tk.BOTTOM,expand=True,fill=tk.BOTH)
        x_offset = top.winfo_x()
        width = top.winfo_width()
        y_offset = top.winfo_y()
        self.geometry("+{}+{}".format(x_offset+width, y_offset))
        self.protocol('WM_DELETE_WINDOW',top.toggle_log)

    def refresh(self,stack):
        self.script.delete(1.0,tk.END)
        self.script.insert(tk.INSERT,'\n'.join(stack))
