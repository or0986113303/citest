class Model(object):
    def __init__(self, imagewidth, imageheight, cameraid):
        self.__imagewidth__ = imagewidth
        self.__imageheight__ = imageheight
        self.__cameraID__ = cameraid
        self.__sourceimage__ = None
        self.__grayimage__ = None
        self.__smoothimage__ = None
        self.__resultimage__ = None
        self.__edgeimage__ = None
        self.rect = None
        self.frame = None
        self.statusimage = None
        self.MTF50result = {"lefttop" : None, "leftbutton" : None \
        , "righttop" : None, "rightbutton" : None, "center" : None}
        self.MTF80result = {"lefttop" : None, "leftbutton" : None \
        , "righttop" : None, "rightbutton" : None, "center" : None}
        self.DFTresult = {"lefttop" : None, "leftbutton" : None \
        , "righttop" : None, "rightbutton" : None, "center" : None, "full" : None}
        
        
        
        
    def __del__(self):
        del self.__imagewidth__
        del self.__imageheight__
        del self.__cameraID__
        del self.__sourceimage__
        del self.__grayimage__
        del self.__smoothimage__
        del self.__resultimage__
        del self.__edgeimage__
        del self.rect
        del self.frame
    
    def getEdgeImage(self):
        return self.__edgeimage__

    def setEdgeImage(self, value):
        self.__edgeimage__ = value

    def setResultImage(self, value):
        self.__resultimage__ = value

    def getResultImage(self):
        return self.__resultimage__

    def getSourceImage(self):
        return self.__sourceimage__
    
    def setSourceImage(self, value):
        self.__sourceimage__ = value
    
    def getGrayImage(self):
        return self.__grayimage__
    
    def setGrayImage(self, value):
        self.__grayimage__ = value
    
    def getSmoothImage(self):
        return self.__smoothimage__
    
    def setSmoothImage(self, value):
        self.__smoothimage__ = value

    def getImageWidth(self):
        return self.__imagewidth__
    
    def setImageWidth(self, value):
        self.__imagewidth__ = value
    
    def getImageHeight(self):
        return self.__imageheight__
    
    def setImageHeight(self, value):
        self.__imageheight__ = value
    
    def getCameraID(self):
        return self.__cameraID__
    
    def setCameraID(self, value):
        self.__cameraID__ = value