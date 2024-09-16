import openSIMS as S
import matplotlib.pyplot as plt
import tests

t = tests.Test()

if True:
    import openSIMS as S
    S.set('instrument','Cameca')
    S.set('path','/home/pvermees/git/openSIMS/data/Cameca_UPb')
    S.read()
    S.set('method','U-Pb',U='238U',UO='238U 16O2',Pb204='204Pb',Pb206='206Pb',Pb207='207Pb')
    S.gui()
else:
    t.test_methodPairing()
