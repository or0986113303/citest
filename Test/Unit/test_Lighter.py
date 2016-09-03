from nose2 import config
from nose2.compat import unittest

from Control import Lighter

class LighterTest(unittest.TestCase):
    tags = ['unit']

    def setUp(self):
        self.parameter = {"Lighter1Port" : "COM1", "Lighter1BaudRate" : 9600,\
        "Lighter2Port" : "COM2", "Lighter2BaudRate" : 9600,\
        "Lighter3Port" : "COM3", "Lighter3BaudRate" : 9600}
        self.connectresult = 0
        self.disconnectresult = 0
        self.lighter = Lighter.Control()
    
    def test_as_connect(self):
        self.assertEqual(self.lighter.connect(self.parameter), self.connectresult)

    def test_as_disconnect(self):
        self.assertEqual(self.lighter.disconnect(), self.disconnectresult)
    
    def test_as_setvalue(self):
        pass

if __name__ == '__main__':
    unittest.main()