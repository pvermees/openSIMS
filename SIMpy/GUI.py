import tkinter as tk
import tkinter.filedialog as fd
import tkinter.ttk as ttk

class gui(tk.Tk):

    def __init__(self,settings):
        super().__init__()
        self.title('SIMpy')
        self.sp = settings
        self.stack = ["from SIMpy import SIMpy",
                      "sp = SIMpy(gui=True)"]
        self.create_open_button()
        self.create_method_button()
        self.create_log_button()
        self.create_exit_button()

    def run(self,cmd):
        self.stack.append(cmd)
        print(self.stack)
        exec('self.' + cmd)

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
        button = ttk.Button(self,text='Log',command=self.on_log)
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

    def on_log(top):
        log = LogWindow(top)
        
class MethodWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__(top)
        self.title('method')
        print(top.sp.data_dir)
        ttk.Button(self,text='Close',command=self.destroy).pack()
