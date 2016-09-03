from nose2 import config
from nose2.compat import unittest

from Control import Camera

class CameraTest(unittest.TestCase):
    tags = ['unit']

    def setUp(self):
        self.connectresult = True
        self.disconnectresult = True
        self.camera = Camera.Control(720, 480, 0)
    
    def test_as_connect(self):
        self.assertEqual(self.camera.connect(), self.connectresult)

    def test_as_disconnect(self):
        self.assertEqual(self.camera.disconnect(), self.disconnectresult)
    

if __name__ == '__main__':
    unittest.main()