import cv2
import numpy as np

from Model import Camera

class Control(object):
    def __init__(self, imagewidth, imageheight, cameraid):
        self.__cameramodel__ = Camera.Model(imagewidth, imageheight, cameraid)
        self.__capture__ = None 
        self.__colorlist__ = {"RGB" : cv2.COLOR_BGR2RGB, "Gray" : cv2.COLOR_BGR2GRAY}
        self.__isSuccess__ = False
    
    def connect(self):
        self.__capture__ = cv2.VideoCapture(self.__cameramodel__.getCameraID())
        self.__capture__.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.__cameramodel__.getImageWidth())
        self.__capture__.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.__cameramodel__.getImageHeight())
        if self.__capture__.isOpened() :
            self.__isSuccess__ = True
        else :
            self.__isSuccess__ = False
        #try :
        #    self.grabFrame()
        #    self.__isSuccess__ = True
        #except :
        #    self.__isSuccess__ = False
        
        return self.__isSuccess__

    def disconnect(self):
        #del self.__capture__
        self.__isSuccess__ = True
        return self.__isSuccess__

    def __del__(self):
        #self.__capture__.release() 
        del self.__cameramodel__
        del self.__capture__
    
    def __autocanny__(self, image, sigma=0.33):
        # compute the median of the single channel pixel intensities
        v = np.median(image)
        # apply automatic Canny edge detection using the computed median
        lower = 200#int(max(0, (1.0 - sigma) * v))
        upper = 255#int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)
        # return the edged image
        return edged

    def grabFrame(self):
        self.__cameramodel__.ret, self.__cameramodel__.frame = self.__capture__.read()
        self.__cameramodel__.setSourceImage(self.__cameramodel__.frame)
        self.__cameramodel__.statusimage = self.__cameramodel__.frame
        self.__cameramodel__.setSourceImage(cv2.cvtColor(self.__cameramodel__.getSourceImage(), self.__colorlist__["RGB"]))
        self.__cameramodel__.setGrayImage(cv2.cvtColor(self.__cameramodel__.getSourceImage(), self.__colorlist__["Gray"]))
        self.__cameramodel__.setSmoothImage(cv2.GaussianBlur(self.__cameramodel__.getGrayImage(),(5,5),0))
        '''
        try :
            self.__cameramodel__.ret, self.__cameramodel__.frame = self.__capture__.read()
            self.__cameramodel__.setSourceImage(self.__cameramodel__.frame)
            self.__cameramodel__.statusimage = self.__cameramodel__.frame
            self.__cameramodel__.setSourceImage(cv2.cvtColor(self.__cameramodel__.getSourceImage(), self.__colorlist__["RGB"]))
            self.__cameramodel__.setGrayImage(cv2.cvtColor(self.__cameramodel__.getSourceImage(), self.__colorlist__["Gray"]))
            self.__cameramodel__.setSmoothImage(cv2.GaussianBlur(self.__cameramodel__.getGrayImage(),(5,5),0))
            self.isSuccess = True
        except :
            self.isSuccess = False
        '''
        
    
    def getStatusImage(self, value):
        self.__cameramodel__.statusimage = np.zeros(( \
        self.__cameramodel__.frame.shape[0], \
        self.__cameramodel__.frame.shape[1], \
        self.__cameramodel__.frame.shape[2]), np.uint8)
        self.__cameramodel__.statusimage.fill(255)
        cv2.putText(self.__cameramodel__.statusimage, \
        value, (self.__cameramodel__.frame.shape[1]/2 - 80, self.__cameramodel__.frame.shape[0]/2) \
        , cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2)
        return self.__cameramodel__.statusimage
        
    def setCuttrntEdgeImage(self, value):
        self.__cameramodel__.setEdgeImage(value)

    def getCurrentEdgeImage(self):
        return self.__cameramodel__.getEdgeImage()

    def getCurrentGrayImage(self):
        return self.__cameramodel__.getGrayImage()
    
    def getCurrentRGBImage(self):
        return self.__cameramodel__.getSourceImage()
    
    def getSmoothGrayImage(self):
        return self.__cameramodel__.getSmoothImage()
    
    def getMTF50Result(self, location):
        return self.__cameramodel__.MTF50result[location]
    
    def setMTF50Result(self, location, value):
        self.__cameramodel__.MTF50result[location] = value
    
    def getMTF80Result(self, location):
        return self.__cameramodel__.MTF80result[location]
    
    def setMTF80Result(self, location, value):
        self.__cameramodel__.MTF80result[location] = value
    
    def getDFTresult(self, location):
        return self.__cameramodel__.DFTresult[location]
    
    def setDFTresult(self, location, value):
        self.__cameramodel__.DFTresult[location] = value
        