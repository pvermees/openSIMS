import openSIMS as S
import numpy as np
from . import Refmats
from scipy.optimize import minimize

def misfit4(pars,standards):
    b, a, B  = pars[0:3]
    A = dict()
    for i, standard in enumerate(standards):
        A[standard] = pars[3+i]
    samples = S.get('samples')
    out = 0.0
    for sample in samples:
        if sample.group == 'sample':
            pass
        else:
            stnd = sample.group
            U_obs = sample.cps('U')['cps']
            UO_obs = sample.cps('UO')['cps']
            Pb4_obs = sample.cps('Pb204')['cps']
            Pb6 = sample.cps('Pb206')
            Pb6_obs = Pb6['cps']
            a0 = Refmats.get_values('U-Pb',stnd)['P64_0']
            drift = np.exp(a+b*Pb6['time'])
            x, ss = get_x(U_obs,UO_obs,Pb6_obs,Pb4_obs,a0,A[stnd],B,drift)
            out += ss
    return out

def get_x(U_obs,UO_obs,Pb6_obs,Pb4_obs,a0,A,B,d):
    init = np.log(U_obs/UO_obs)
    res = minimize(SS,init,method='BFGS',jac='dSSdx',
                   args=(U_obs,UO_obs,Pb6_obs,Pb4_obs,a0,A,B,d))
    return res.x, res.fun

def SS(x,U_obs,UO_obs,Pb6_obs,Pb4_obs,a0,A,B,d):
    u = get_u(x,U_obs,UO_obs,Pb6_obs,Pb4_obs,a0,A,B,d)
    UO_pred = u*x
    Pb6_pred = u*d*A*x**B
    ss = (Pb6_obs-Pb6_pred)**2 + (UO_obs-UO_pred)**2 + (U_obs-u)**2
    return sum(ss)
    
def dSSdx(x,U_obs,UO_obs,Pb6_obs,Pb4_obs,a0,A,B,d):
    u = get_u(x,U_obs,UO_obs,Pb6_obs,Pb4_obs,a0,A,B,d)
    term1 = -2*A*B*d*u*x**(B-1) * ((-A*d*u*x**B)-Pb4_obs*a0+Pb6_obs)
    term2 = -2*u*(UO_obs-u*x)
    return sum(term1 + term2)

def get_u(x,U_obs,UO_obs,Pb6_obs,Pb4_obs,a0,A,B,d):
    num = -((A*Pb4_obs*a0-A*Pb6_obs)*d*x**B-UO_obs*x-U_obs)
    den = (A**2*d**2*x**(2*B)+x**2+1)
    return num/den
