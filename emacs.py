import openSIMS as S
import matplotlib.pyplot as plt
import tests

t = tests.Test()

if True:
    S.set('instrument','Cameca')
    S.set('path','/home/pvermees/git/openSIMS/data/Cameca_O')
    S.read()
    S.add_method('O',O16='16O',O17='17O',O18='18O')
    S.standards(NBS28=[0,2,3,5,7])
    S.gui()
else:
    t.test_multiple_methods()
