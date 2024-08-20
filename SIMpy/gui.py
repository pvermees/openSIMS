import tkinter as tk
import tkinter.filedialog as fd

def on_open():
    fd.askdirectory()

def on_method():
    method = tk.Tk()
    method.title("method")

    test_button = tk.Button(method,text="Test",command=method.destroy).pack()
    
def start():
    root = tk.Tk()
    root.title("SIMpy")

    open_button = tk.Button(root,text="Open",command=on_open).pack()
    method_button = tk.Button(root,text="Method",command=on_method).pack()
    exit_button = tk.Button(root,text="Exit",command=root.destroy).pack()

    root.mainloop()
