import openSIMS as S
import numpy as np
from . import Refmats

def misfit3(pars,standards,standard_names):
    nA = len(standard_names)
    b = pars[0]
    B = pars[1]
    A = dict(zip(standard_names,pars[2:]))
    SS = 0.0
    for sname, standard in standards.items():
        U, UO, Pb4, Pb6, t = standard.misfit_data_UPb()
        a0 = Refmats.get_values('U-Pb',standard.group)['P64_0']
        drift = np.exp(b*t/60)
        xo = np.log(UO) - np.log(U)
        yo = np.log(drift*Pb6-a0*Pb4) - np.log(U)
        yp = A[standard.group]+B*xo
        SS += sum((yp-yo)**2)
    return SS
