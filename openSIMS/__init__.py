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

def plot(i=None,sname=None,show=True,num=None):
    if i is None and sname is None:
        i = __S.i
    return __S.plot(i=i,sname=sname,show=show,num=num)

def gui():
    GUI.gui()

def TODO():
    pass
