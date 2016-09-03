from nose2 import config
from nose2.compat import unittest

from Control import Ammeter

class AmmeterTest(unittest.TestCase):
    tags = ['unit']

    def setUp(self):
        self.connectresult = True
        self.disconnectresult = True
        self.ammeter = Ammeter.Control()
    
    def test_as_connect(self):
        self.assertEqual(self.ammeter.connect(comport = "COM1", baudrate = 9600, type = "GDM-360"), self.connectresult)

    def test_as_disconnect(self):
        self.assertEqual(self.ammeter.disconnect(), self.disconnectresult)
    

if __name__ == '__main__':
    unittest.main()