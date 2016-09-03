class Model(object):
    def __init__(self):
        self.__patternpoints__ = None
        self.caculatecenter = {"x" : 0, "y" : 0}
        self.__patternimage__ = None
        self.__sensorsize__ = None
        self.colorshadeareasource = {"lefttop" : None, "leftbutton" : None, "righttop" : None, "rightbutton" : None}
        self.colorshadearearesult = {"lefttop" : None, "leftbutton" : None, "righttop" : None, "rightbutton" : None}
        self.colorshadelocation = {"lefttop" : None, "leftbutton" : None, "righttop" : None, "rightbutton" : None}
        self.roitmp = None
        self.element = None
        self.centershiftsqeuere = None
    
    def getSensorSize(self):
        return self.__sensorsize__
    
    def setSensorSize(self, value):
        self.__sensorsize__ = value

    def getPatternImage(self):
        return self.__patternimage__
    
    def setPatternImage(self, value):
        self.__patternimage__ = value

    def getPatternPoints(self):
        return self.__patternpoints__
    
    def setPatternPoints(self, value):
        self.__patternpoints__ = value

    def __del__(self):
        del self.__patternpoints__