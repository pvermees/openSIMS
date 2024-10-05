import matplotlib.pyplot as plt
from .API import Simplex, Settings
from .GUI.Main import gui

__simplex = Simplex.Simplex()
__settings = Settings.Settings()

def set(prop,val):
    setattr(__simplex,prop,val)

def get(prop):
    return getattr(__simplex,prop)

def add_method(method,**kwargs):
    __simplex.methods[method] = __settings.ions2channels(method,**kwargs)

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

def view(i=None,sname=None):
    if i is None and sname is None:
        i = __simplex.i
    return __simplex.view(i=i,sname=sname)

def plot_calibration():
    return __simplex.plot_calibration()

def plot_processed():
    return __simplex.plot_processed()

def process():
    __simplex.process()

def simplex():
    return __simplex

def settings(method=None):
    if method is None:
        return __settings
    else:
        return __settings[method]

def TODO():
    pass
