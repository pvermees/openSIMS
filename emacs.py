import openSIMS as S
import matplotlib.pyplot as plt
import tests

t = tests.Test()

if True:
    S.set('instrument','Cameca')
    S.set('path','/home/pvermees/git/openSIMS/data/Cameca_UThPb')
    S.read()
    S.add_method('Th-Pb',Th='232Th',ThOx='232Th 16O2',Pb208='208Pb',Pb204='204Pb')
    S.standards(_44069=[0,1,3,4,6,7,9,10,12])
    S.calibrate()
    S.gui()
else:
    t.test_process()

