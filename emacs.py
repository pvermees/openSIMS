import openSIMS as S
import matplotlib.pyplot as plt
import tests

t = tests.Test()

if True:
    S.set('instrument','Cameca')
    S.gui()
else:
    t.test_multiple_methods()
