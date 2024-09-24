import json
import os
import pkgutil

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
    fname = os.path.join('..','Settings','methods.json')
    data = pkgutil.get_data(__name__,fname)
    json_string = data.decode('utf-8')
    pars = json.loads(json_string)
    return pars[m][setting]
