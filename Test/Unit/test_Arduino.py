from nose2 import config
from nose2.compat import unittest

from Control import Arduino

class ArduinoTest(unittest.TestCase):
    tags = ['unit']

    def setUp(self):
        self.connectresult = True
        self.disconnectresult = True
        self.arduino = Arduino.Control()
    
    def test_as_connect(self):
        self.assertEqual(self.arduino.connect("COM4", 9600), self.connectresult)

    def test_as_disconnect(self):
        self.assertEqual(self.arduino.disconnect(), self.disconnectresult)
    

if __name__ == '__main__':
    unittest.main()