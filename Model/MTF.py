class Model(object):
    def __init__(self, imagewidth, imageheight):
        self.__imagewidth__ = imagewidth
        self.__imageheight__ = imageheight
        self.__sourceimage__ = None
        self.__DFTimage__ = None
        self.__FFTimage__ = None
        self.__resultimage__ = None
        self.__MTFImage__ = None
        self.globalfftvalue = 0

    def getSourceImage(self):
        return self.__sourceimage__
    
    def setSourceImage(self, value):
        self.__sourceimage__ = value

    def getDFTImage(self):
        return self.__DFTimage__
    
    def getFFTImage(self):
        return self.__FFTimage__
    
    def getMTFImage(self):
        return self.__MTFImage__
    
    def setImageWidth(self, value):
        self.__imagewidth__ = value
    
    def getImageWidth(self):
        return self.__imagewidth__
    
    def setImageHeight(self, value):
        self.__imageheight__ = value
    
    def getImageHeight(self):
        return self.__imageheight__
