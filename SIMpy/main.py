import SIMpy.GUI as GUI

class SIMpy:
    
    def __init__(self,gui=False):
        self.datadir = ''
        self.method = ''
        if gui: self.gui = GUI.gui(self)
