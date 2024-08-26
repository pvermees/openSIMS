import openSIMS, tests
import matplotlib.pyplot as plt

t = tests.Test()

if False:
    t.testRun()
elif False:
    t.testSample()
    plt.show()
else:
    sp = openSIMS.simplex(gui=True)
