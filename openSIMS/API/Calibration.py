import copy
import openSIMS as S
from . import Geochron, Stable, PbPb

class Standards():

    def __init__(self,simplex,method):
        self.method = method
        self.pars = simplex.get_pars(method)
        if method in simplex.results:
            self.results = simplex.results[method]
        else:
            self.results = None
        self.samples = copy.copy(simplex.samples)
        for name, sample in simplex.samples.items():
            if sample.group == 'sample' or name in simplex.ignore:
                self.samples.drop(name,inplace=True)

class GeochronStandards(Standards,Geochron.Geochron,Geochron.Calibrator):
    pass

class StableStandards(Standards,Stable.Stable,Stable.Calibrator):
    pass

class PbPbStandards(Standards,PbPb.PbPb,PbPb.Calibrator):
    pass

def get_standards(simplex,method=None):
    if method is None:
        method = S.list_methods()[0]
    datatype = S.settings(method)['type']
    if datatype == 'geochron':
        return GeochronStandards(simplex,method)
    elif datatype == 'stable':
        return StableStandards(simplex,method)
    elif datatype == 'geochron_PbPb':
        return PbPbStandards(simplex,method)
