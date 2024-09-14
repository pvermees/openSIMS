import unittest
import matplotlib.pyplot as plt
from openSIMS import Cameca, SHRIMP, Sample
import openSIMS as S

class Test(unittest.TestCase):

    def test_newCamecaSHRIMPinstance(self):
        cam = S.Cameca.Cameca_Sample()
        shr = S.SHRIMP.SHRIMP_Sample()
        self.assertIsInstance(cam,S.Sample.Sample)
        self.assertIsInstance(cam,S.Sample.Sample)

    def test_openCamecaASCfile(self):
        samp = S.Cameca.Cameca_Sample()
        samp.read("data/Cameca_UPb/Plesovice@01.asc")
        self.assertEqual(samp.signal.size,84)
        samp.plot(show=False)

    def test_createButDontShowPlot(self):
        self.loadCamecaData()
        S.plot(show=False)

    def test_gui(self):
        self.loadCamecaData()
        S.gui()

    def loadCamecaData(self):
        S.set('instrument','Cameca')
        S.set('path','data/Cameca_UPb')
        S.read()        
        
if __name__ == '__main__':
    unittest.main()
