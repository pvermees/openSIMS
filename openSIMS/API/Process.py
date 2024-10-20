import copy
import openSIMS as S
from . import Geochron, Stable, PbPb

class Samples:

    def __init__(self,simplex,method):
        self.method = method
        self.pars = simplex.get_pars(method)
        if method in simplex.results:
            self.results = simplex.results[method]
        else:
            self.results = None
        self.samples = copy.copy(simplex.samples)

class GeochronSamples(Samples,Geochron.Geochron,Geochron.Processor):
    pass

class StableSamples(Samples,Stable.Stable,Stable.Processor):
    pass

class PbPbSamples(Samples,PbPb.PbPb,PbPb.Processor):
    pass

def get_samples(simplex,method=None):
    if method is None:
        method = S.list_methods()[0]
    datatype = S.settings(method)['type']
    if datatype == 'geochron':
        return GeochronSamples(simplex,method)
    elif datatype == 'stable':
        return StableSamples(simplex,method)
    elif datatype == 'geochron_PbPb':
        return PbPbSamples(simplex,method)
    else:
        raise ValueError('Unrecognised data type')
