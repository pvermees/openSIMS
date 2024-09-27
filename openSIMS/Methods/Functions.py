import openSIMS as S
import numpy as np

def calibration_data_UPb(standard,b):
    U = standard.cps('U')
    UOx = standard.cps('UOx')
    Pb4 = standard.cps('Pb204')
    Pb6 = standard.cps('Pb206')
    drift = np.exp(b*Pb6['time']/60)
    a0 = S.settings('UPb').get_a0(standard.group)
    x = np.log(UOx['cps']) - np.log(U['cps'])
    y = np.log(drift*Pb6['cps']-a0*Pb4['cps']) - np.log(U['cps'])
    return x, y
