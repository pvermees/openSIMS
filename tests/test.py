import unittest
import SIMpy as sp

class TestGui(unittest.TestCase):
    def test_gui(self):
        try:
            sp.gui.start()
            sp.gui.on_method()
            self.root.assertFalse(self.root.winfo_exists())
        except Exception as e:
            self.fail(f"on_exit raised an exception: {e}")

    def test_test(self):
        self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()
