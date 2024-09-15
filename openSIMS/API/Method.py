class method:

    def __init__(self,name,**kwargs):
        keys = method2ions(name)
        self.name = name
        self.ions = dict()
        for key, val in kwargs.items():
            if key in keys:
                self.ions[key] = val
            else:
                self.ions[key] = None

def method2ions(m):
    if m=='U-Pb':
        return ['U','UO','Pb204','Pb206','Pb207']
    elif m=='Th-Pb':
        return ['Th','ThO','Pb204','Pb208']
    elif m=='O':
        return ['O16','O17','O18']
    elif m=='S':
        return ['S32','S33','S34','S36']
    else:
        raise ValueError('Invalid method.')
