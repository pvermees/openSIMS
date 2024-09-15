import openSIMS as S
import pandas as pd

class method:

    def __init__(self,meth,**kwargs):
        self.ions = dict()
        ions = self.method2ions(meth)
        for key, val in kwargs.items():
            if key in ions:
                self.ions[key] = val
            else:
                self.ions[key] = None

    def method2ions(self,meth):
        if meth=='U-Pb':
            return ['U','UO','Pb204','Pb206','Pb207']
        elif meth=='Th-Pb':
            return ['Th','ThO','Pb204','Pb208']
        elif meth=='O':
            return ['O16','O17','O18']
        elif meth=='S':
            return ['S32','S33','S34','S36']
        else:
            return None
