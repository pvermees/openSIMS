import openSIMS as S
import matplotlib.pyplot as plt
import tests

t = tests.Test()

if False:
    S.gui()
else:
    t.test_calibrate_O()
    plt.show()
