import SIMplex, tests
import matplotlib.pyplot as plt

t = tests.Test()

if False:
    t.testRun()
elif False:
    t.testSample()
    plt.show()
else:
    sp = SIMplex.simplex(gui=True)
