import unittest
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import openSIMS as S
from openSIMS.API import Cameca, SHRIMP, Calibration, Process, Sample

class Test(unittest.TestCase):

    def loadCamecaData(self):
        S.set('instrument','Cameca')
        S.set('path','data/Cameca_UPb')
        S.read()

    def loadCamecaUPbMethod(self):
        self.loadCamecaData()
        S.add_method('U-Pb',
                     U238='238U',UOx='238U 16O2',
                     Pb204='204Pb',Pb206='206Pb')
        
    def loadOxygen(self):
        S.set('instrument','Cameca')
        S.set('path','data/Cameca_O')
        S.read()
        S.add_method('O',O16='16O',O17='17O',O18='18O')
        
    def loadMonaziteData(self):
        S.set('instrument','Cameca')
        S.set('path','data/Cameca_UThPb')
        S.read()
        S.add_method('U-Pb',
                     U238='238U',UOx='238U 16O2',
                     Pb204='204Pb',Pb206='206Pb')
        S.add_method('Th-Pb',
                     Th232='232Th',ThOx='232Th 16O2',
                     Pb204='204Pb',Pb208='208Pb')
        S.standards(_44069=['44069@1','44069@2','44069@3','44069@4','44069@5',
                            '44069@6','44069@7','44069@8','44069@9'])

    def setCamecaStandards(self):
        self.loadCamecaUPbMethod()
        S.standards(Plesovice=[0,1,3])

    def calibrate_O(self):
        self.loadOxygen()
        S.standards(NBS28=['NBS28@1','NBS28@2','NBS28@3','NBS28@4','NBS28@5'])
        S.calibrate()

    def calibrate_O_2_standards(self):
        self.loadOxygen()
        S.standards(NBS28=['NBS28@1','NBS28@2','NBS28@3','NBS28@4','NBS28@5'],
                    Qinghu=['Qinghu@1','Qinghu@2','Qinghu@3'])
        S.calibrate()
        
    def process_monazite(self):
        self.loadMonaziteData()
        S.calibrate()
        S.process()
        
    def process_O(self):
        self.calibrate_O()
        S.process()

    def process_O_2_standards(self):
        self.calibrate_O_2_standards()
        S.process()
        
    def test_newCamecaSHRIMPinstance(self):
        cam = Cameca.Cameca_Sample()
        shr = SHRIMP.SHRIMP_Sample()
        self.assertIsInstance(cam,Sample.Sample)
        self.assertIsInstance(shr,Sample.Sample)

    def test_openCamecaASCfile(self):
        samp = Cameca.Cameca_Sample()
        samp.read("data/Cameca_UPb/Plesovice@01.asc")
        self.assertEqual(samp.signal.size,84)
        samp.view()

    def test_view(self):
        self.loadCamecaData()
        S.view()
        self.loadOxygen()
        S.view()

    def test_methodPairing(self):
        self.loadCamecaUPbMethod()
        self.assertEqual(S.get('methods')['U-Pb']['UOx'],'238U 16O2')

    def test_setStandards(self):
        self.setCamecaStandards()
        self.assertEqual(S.get('samples').iloc[0].group,'Plesovice')

    def test_settings(self):
        DP = S.settings('U-Pb').get_DP('Plesovice')
        y0 = S.settings('U-Pb').get_y0('Plesovice')
        self.assertEqual(DP,0.05368894845896288)
        self.assertEqual(y0,18.18037)

    def test_cps(self):
        self.loadCamecaUPbMethod()
        Pb206 = S.get('samples')['Plesovice@01'].cps('U-Pb','Pb206')
        self.assertEqual(Pb206.loc[0,'cps'],1981.191294204482)

    def test_misfit(self,b=0.0):
        self.loadMonaziteData()
        standards = Calibration.get_standards(S.simplex())
        np.random.seed(0)
        for name, standard in standards.samples.items():
            x,y = standards.get_xy(name,b=0.0)
            plt.scatter(x,y,color=np.random.rand(3,))

    def test_calibrate_UPb(self):
        self.setCamecaStandards()
        S.calibrate()
        pars = S.get('pars')['U-Pb']
        self.assertEqual(pars['b'],0.000375)

    def test_calibrate_O(self):
        self.calibrate_O()
        S.plot_calibration()

    def test_calibrate_O_2_standards(self):
        self.calibrate_O_2_standards()
        S.plot_calibration()

    def test_multiple_methods(self):
        self.loadMonaziteData()
        S.add_method('U-Pb',
                     U238='238U',UOx='238U 16O2',
                     Pb204='204Pb',Pb206='206Pb')
        S.calibrate()
        S.plot_calibration()

    def test_process_monazite(self):
        self.process_monazite()
        S.plot_processed()

    def test_process_O(self):
        self.process_O()
        S.plot_processed()
        
    def test_export_monazite(self):
        self.process_monazite()
        S.simplex().export_csv('tests/out/monazite.csv',fmt='U-Pb-2')

    def test_export_O(self):
        self.process_O()
        S.simplex().export_csv('tests/out/O.csv')
        
if __name__ == '__main__':
    unittest.main()
