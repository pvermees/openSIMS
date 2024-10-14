import matplotlib.pyplot as plt
from .API import Simplex, Settings
from .GUI import Main

__simplex = Simplex.Simplex()
__settings = Settings.Settings()

def gui():
    Main.gui()

def set(prop,val):
    setattr(__simplex,prop,val)

def get(prop):
    return getattr(__simplex,prop)

def add_method(method,**kwargs):
    __simplex.methods[method] = __settings.ions2channels(method,**kwargs)

def list_methods():
    return list(__simplex.methods.keys())
    
def remove_method(method):
    del __simplex.methods[method]
    
def standards(**kwargs):
    __simplex.set_groups(**kwargs)
    
def reset():
    __simplex.reset()

def read():
    __simplex.read()

def calibrate():
    __simplex.calibrate()

def process():
    __simplex.process()

def view(i=None,sname=None):
    if i is None and sname is None:
        i = __simplex.i
    return __simplex.view(i=i,sname=sname)

def plot_calibration(method=None):
    return __simplex.plot_calibration(method=method)

def plot_processed(method=None):
    return __simplex.plot_processed(method=method)

def export_csv(path,fmt='default'):
    __simplex.export_csv(path,fmt=fmt)

def simplex():
    return __simplex

def settings(method=None):
    if method is None:
        return __settings
    else:
        return __settings[method]

def TODO():
    pass
