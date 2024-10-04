import copy
import openSIMS as S
from . import Geochron, Stable

class Standards:

    def __init__(self,simplex,method):
        self.pars = simplex.get_pars(method)
        self.method = method
        self.samples = copy.copy(simplex.samples)
        for sname, sample in simplex.samples.items():
            if sample.group == 'sample' or sname in simplex.ignore:
                self.samples.drop(sname,inplace=True)

class GeochronStandards(Standards,Geochron.Geochron,Geochron.Calibrator):
    pass

class StableStandards(Standards,Stable.Stable,Stable.Calibrator):
    pass

def getStandards(simplex,method=None):
    if method is None:
        method = list(simplex.methods.keys())[0]
    datatype = S.settings(method)['type']
    if datatype == 'geochron':
        return GeochronStandards(simplex,method)
    elif datatype == 'stable':
        return StableStandards(simplex,method)
    else:
        raise ValueError('Unrecognised data type')
