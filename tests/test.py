import unittest
import time
import SIMplex
import matplotlib.pyplot as plt
from SIMplex.Sample import Sample

class Test(unittest.TestCase):

    def testSample(self):
        cam = SIMplex.Cameca.Cameca_Sample()
        shr = SIMplex.SHRIMP.SHRIMP_Sample()
        self.assertIsInstance(cam,Sample)
        self.assertIsInstance(cam,Sample)

    def testSample(self):
        samp = SIMplex.Cameca.Cameca_Sample()
        samp.read("data/Cameca_UPb/Plesovice@01.asc")
        self.assertEqual(samp.signal.size,84)
        samp.plot(show=False)

    def testRun(self):
        sp = SIMplex.simplex()
        sp.set_instrument('Cameca')
        sp.set_path('data/Cameca_UPb')
        sp.read()
        sp.plot()

if __name__ == '__main__':
    unittest.main()
