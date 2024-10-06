import openSIMS as S
import matplotlib.pyplot as plt
import tests

t = tests.Test()

if False:
    S.gui()
else:
    t.test_process_O()
    print(S.get('results'))
