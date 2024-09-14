import openSIMS as S
import matplotlib.pyplot as plt
import tests

t = tests.Test()

if False:
    t.newCamecaSHRIMPinstance()
elif False:
    t.createButDontShowPlot()
    plt.show()
else:
    S.gui()