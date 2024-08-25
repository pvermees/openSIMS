import unittest
import SIMplex as sp
from SIMplex.Sample import Sample

class Test(unittest.TestCase):

    def testSample(self):
        cam = sp.Cameca.Cameca_Sample()
        shr = sp.SHRIMP.SHRIMP_Sample()
        self.assertIsInstance(cam,Sample)
        self.assertIsInstance(cam,Sample)

    def testCameca(self):
        samp = sp.Cameca.Cameca_Sample()
        samp.read("data/Cameca_UPb/Plesovice@01.asc")
        self.assertEqual(samp.signal.size,84)
        samp.plot()

if __name__ == '__main__':
    unittest.main()
