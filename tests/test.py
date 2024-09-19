import unittest
import matplotlib.pyplot as plt
from openSIMS.API import Cameca, Method, SHRIMP, Sample, Simplex, Refmats
import openSIMS as S

class Test(unittest.TestCase):

    def loadCamecaData(self):
        S.set('instrument','Cameca')
        S.set('path','data/Cameca_UPb')
        S.read() 

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

    def test_getCamecaChannels(self):
        self.loadCamecaData()
        self.assertEqual(S.get('channels'),
                         ['90Zr2 16O','92Zr2 16O','200.5','94Zr2 16O',
                          '204Pb','206Pb','207Pb','208Pb','238U',
                          '232Th 16O2','238U 16O2','270.1'])

    def test_methodPairing(self):
        S.method('U-Pb',
                 U='238U',UO='238U 16O2',
                 Pb204='204Pb',Pb206='206Pb',Pb207='207Pb')
        self.assertEqual(S.get('method').ions['UO'],'238U 16O2')

    def test_setStandards(self):
        S.standards(Plesovice=[0,1,3])
        self.assertEqual(S.get('samples').iloc[0].group,'Plesovice')

    def test_loadRefMats(self):
        NBS28 = Refmats.get_values('O','NBS28')
        self.assertEqual(NBS28['O17/O16'],4.79)

    def test_getRefmatNames(self):
        standards = Refmats.get_names('O')
        print(standards)
        
if __name__ == '__main__':
    unittest.main()
