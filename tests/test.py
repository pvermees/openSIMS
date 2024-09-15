import unittest
import matplotlib.pyplot as plt
from openSIMS.API import Cameca, SHRIMP, Sample, Simplex
import openSIMS as S

class Test(unittest.TestCase):

    def test_newCamecaSHRIMPinstance(self):
        cam = Cameca.Cameca_Sample()
        shr = SHRIMP.SHRIMP_Sample()
        self.assertIsInstance(cam,Sample.Sample)
        self.assertIsInstance(cam,Sample.Sample)

    def test_openCamecaASCfile(self):
        samp = Cameca.Cameca_Sample()
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
