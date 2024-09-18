from .API import Simplex, Method
from .GUI.Main import gui

__S = Simplex.simplex()

def set(prop,val):
    setattr(__S,prop,val)

def get(prop):
    if prop == 'channels':
        return __S.channels()
    else:
        return getattr(__S,prop)

def method(val,**kwargs):
    __S.method = Method.method(val,**kwargs)

def standards(**kwargs):
    __S.set_groups(**kwargs)
    
def reset():
    __S.reset()

def read():
    __S.read()

def plot(i=None,sname=None,show=True,num=None):
    if i is None and sname is None:
        i = __S.i
    return __S.plot(i=i,sname=sname,show=show,num=num)

def TODO():
    pass
