class method:

    def __init__(self,name,**kwargs):
        keys = get(name,'ions')
        self.name = name
        self.ions = dict()
        for key, val in kwargs.items():
            if key in keys:
                self.ions[key] = val
            else:
                self.ions[key] = None

    def get(self,setting):
        return get(self.name,setting)

def get(m,setting):
    pars = {'U-Pb': {'ions': ['U','UO','Pb204','Pb206','Pb207'],
                     'y0': 'Pb64_0',
                     'lambda': 0.000155125},
            'Th-Pb': {'ions': ['Th','ThO','Pb204','Pb208'],
                      'y0': 'Pb84_0',
                      'lambda': 0.0000495},
            'O': {'ions': ['O16','O17','O18']},
            'S': {'ions': ['S32','S33','S34','S36']}}
    return pars[m][setting]
