import io
import json
import pandas as pd
import numpy as np
from importlib.resources import files

class Settings(dict):
    
    def __init__(self):
        super().__init__()
        method_file = files('openSIMS.Methods').joinpath('methods.json')
        json_string = method_file.read_text()
        methods = json.loads(json_string)
        for method, pars in methods.items():
            if pars['type'] == 'geochron':
                self[method] = geochron_setting(method,pars)
            elif pars['type'] == 'stable':
                self[method] = stable_setting(method,pars)
            else:
                raise ValueError('Invalid method type')
            
    def ions2channels(self,method,**kwargs):
        if method not in self.keys():
            raise ValueError('Invalid method')
        else:
            channels = dict()
            for ion, channel in kwargs.items():
                if ion in self[method]['ions']:
                    channels[ion] = channel
                else:
                    channels[ion] = None
        return channels

class setting(dict):
    
    def __init__(self,method,pars):
        super().__init__(pars)
        f = files('openSIMS.Methods.Refmats').joinpath(method + '.csv')
        csv_string = f.read_text()
        csv_stringio = io.StringIO(csv_string)
        self['refmats'] = pd.read_csv(csv_stringio,index_col=0)

class geochron_setting(setting):

    def __init__(self,method,pars):
        super().__init__(method,pars)

    def get_DP(self,refmat):
        L = self['lambda']
        t = self['refmats']['t'][refmat]
        return np.exp(L*t) - 1

    def get_y0(self,refmat):
        y0 = self['y0']
        return self['refmats'][y0][refmat]
        
class stable_setting(setting):

    def __init__(self,method,pars):
        super().__init__(method,pars)

    def get_ref(self,refmat):
        pass
