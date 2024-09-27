import tkinter as tk
from . import Main

class HelpWindow(tk.Toplevel):

    def __init__(self,top,item='top'):
        super().__init__(top)
        self.title('Help')
        Main.offset(top,self)
        label = tk.Label(self,text=Help(item),anchor='w',justify='left')
        label.bind('<Configure>', lambda e: label.config(wraplength=label.winfo_width()))
        label.pack(expand=True,fill=tk.BOTH)

def Help(item):
    if item=="top":
        out = "Choose one of the following options:\n" + \
        "1. Open: Load SIMS data. There are two options:\n" + \
        "  - Cameca: select a folder with .asc files\n" + \
        "  - SHRIMP: select an .op or .pd file (TODO)\n" + \
        "2. Method: Select an application and pair the relevant\n" + \
        "   ions with the corresponding mass spectrometer channels.\n" + \
        "3. View: View the time resolved SIMS data\n" + \
        "4. Standards: Mark which analyses correspond to" + \
        "   primary reference materials.\n" + \
        "5. Calibrate: Fit the standards in logratio space\n" + \
        "6. Export: TODO\n" + \
        "7. Log: View, save or run the session log of openSIMS commands\n" + \
        "8. Template: TODO\n" + \
        "9. Settings: TODO\n"
    else:
        pass
    return out
