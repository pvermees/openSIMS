import SIMplex.GUI as GUI

class simplex:
    
    def __init__(self,gui=False):
        self.reset()
        if gui: self.gui = GUI.gui(self)

    def reset(self):
        self.data_dir = ''
        self.instrument = ''
        self.method = ''        

    def set_data_dir(self,value):
        self.data_dir = value

    def get_data_dir(self,value):
        return self.data_dir

    def set_instrument(self,value):
        self.instrument = value

    def get_instrument(self):
        return self.instrument

    def set_method(self,value):
        self.method = value

    def get_method(self):
        return self.method

    def TODO(self):
        pass
