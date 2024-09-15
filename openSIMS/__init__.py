from .API import Simplex, Method
from .GUI.Main import gui

__S = Simplex.simplex()

def set(prop,val,**kwargs):
    if prop == 'method':
        __S.method = Method.method(val,**kwargs)
    else:
        setattr(__S,prop,val)

def get(prop):
    if prop == 'channels':
        return __S.channels()
    else:
        return getattr(__S,prop)

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
