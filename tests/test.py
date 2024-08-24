import unittest

import SIMplex as sp
from SIMplex.Sample import Sample

class Test(unittest.TestCase):

    def test_test(self):
        self.assertEqual(1,1)

    def testCameca(self):
        cam = sp.Cameca.Cameca_Sample()
        shr = sp.SHRIMP.SHRIMP_Sample()
        self.assertIsInstance(cam,Sample)
        self.assertIsInstance(cam,Sample)

if __name__ == '__main__':
    unittest.main()
