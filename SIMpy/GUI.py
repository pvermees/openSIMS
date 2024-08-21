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

    def on_open(self,instrument):
        data_dir = fd.askdirectory()
        self.run("sp.set_instrument('{i}')".format(i=instrument))
        self.run("sp.set_data_dir('{d}')".format(d=data_dir))

    def on_method(self):
        method = MethodWindow(self)
        method.grab_set()

    def toggle_log(self):
        if self.log is None:
            self.log = LogWindow(self)
            self.log.refresh(self.stack)
        else:
            self.log.destroy()
            self.log = None
        
class MethodWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__(top)
        self.title('method')
        ttk.Button(self,text='Close',command=self.destroy).pack()

class LogWindow(tk.Toplevel):
    
    def __init__(self,top):
        super().__init__(top)
        self.title('log')
        x_offset = top.winfo_x()
        width = top.winfo_width()
        y_offset = top.winfo_y()
        self.geometry("+{}+{}".format(x_offset+width, y_offset))
        self.protocol('WM_DELETE_WINDOW',top.toggle_log)
        self.script = st.ScrolledText(self)
        self.script.pack(side=tk.BOTTOM,expand=True,fill=tk.BOTH)
        open_button = ttk.Button(self,text='Open',
                                 command=lambda t=top: self.load(t))
        open_button.pack(expand=True,side=tk.LEFT)
        save_button = ttk.Button(self,text='Save',
                                 command=lambda t=top: self.save(t))
        save_button.pack(expand=True,side=tk.LEFT)
        run_button = ttk.Button(self,text='Run',
                                command=lambda t=top: self.run(t))
        run_button.pack(expand=True,side=tk.LEFT)
        clear_button = ttk.Button(self,text='Clear',
                                  command=lambda t=top: self.clear(t))
        clear_button.pack(expand=True,side=tk.LEFT)

    def refresh(self,stack):
        self.script.delete(1.0,tk.END)
        self.script.insert(tk.INSERT,'\n'.join(stack))

    def load(self,top):
        file = fd.askopenfile()
        top.stack = file.read().splitlines()
        self.refresh(top.stack)
        file.close()

    def save(self,top):
        file = fd.asksaveasfile(mode='w')
        file.writelines('\n'.join(top.stack))
        file.close()

    def run(self,top):
        print("TODO")

    def clear(self,top):
        self.script.delete(1.0,tk.END)
