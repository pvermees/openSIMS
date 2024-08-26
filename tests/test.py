import unittest
import time
import openSIMS
import matplotlib.pyplot as plt
from openSIMS.Sample import Sample

class Test(unittest.TestCase):

    def testSample(self):
        cam = openSIMS.Cameca.Cameca_Sample()
        shr = openSIMS.SHRIMP.SHRIMP_Sample()
        self.assertIsInstance(cam,Sample)
        self.assertIsInstance(cam,Sample)

    def testSample(self):
        samp = openSIMS.Cameca.Cameca_Sample()
        samp.read("data/Cameca_UPb/Plesovice@01.asc")
        self.assertEqual(samp.signal.size,84)
        samp.plot(show=False)

    def testRun(self):
        sp = openSIMS.simplex()
        sp.set_instrument('Cameca')
        sp.set_path('data/Cameca_UPb')
        sp.read()
        sp.plot(show=False)

if __name__ == '__main__':
    unittest.main()
