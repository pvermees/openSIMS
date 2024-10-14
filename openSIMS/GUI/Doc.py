import tkinter as tk
from . import Main

class HelpWindow(tk.Toplevel):

    def __init__(self,top,button,item='top',text=None):
        super().__init__(top)
        self.title('Help')
        Main.offset(button,self)
        self.init_help()
        if text is None:
            text = self.help[item]
        label = tk.Label(self,text=text,anchor='w',justify='left')
        label.bind('<Configure>',
                   lambda e: label.config(wraplength=label.winfo_width()))
        label.pack(expand=True,fill=tk.BOTH)

    def init_help(self):
        self.help = dict()
        self.help["top"] = \
            "Choose one of the following options:\n" + \
            " 1. Open: Load SIMS data. There are two options:\n" + \
            "   - Cameca: select a folder with .asc files\n" + \
            "   - SHRIMP: select an .op or .pd file (TODO)\n" + \
            " 2. Method: Select an application and pair the relevant\n" + \
            "    ions with the corresponding mass spectrometer channels.\n" + \
            " 3. View: View the time resolved SIMS data\n" + \
            " 4. Standards: Mark which analyses correspond to" + \
            "    primary reference materials.\n" + \
            " 5. Calibrate: Fit the standards in logratio space\n" + \
            " 6. Process: Apply the calibration to the samples\n" + \
            " 7. Export: TODO\n" + \
            " 8. Log: View, save or run the session log of openSIMS commands\n" + \
            " 9. Template: TODO\n" + \
            "10. Settings: TODO\n"
        self.help["open"] = \
            "openSIMS currently accepts raw data from two SIMS manufacturers:\n" \
            "1. Cameca: choose a folder containing .asc files.\n" \
            "2. SHRIMP: choose an .op or .pd file containing pooled SIMS data"

