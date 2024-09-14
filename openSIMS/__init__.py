from . import Simplex, GUI, Sample

__S = Simplex.simplex()

def set(prop,val):
    setattr(__S,prop,val)

def get(prop):
    return(getattr(__S,prop))

def reset():
    __S.reset()

def read():
    __S.read()

def plot(show=True,num=None):
    return __S.plot(i=__S.i,show=show,num=num)

def gui():
    GUI.gui()

def TODO():
    pass
