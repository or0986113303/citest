class Model(object):
    def __init__(self):
        self.__result__ = "FAIL"
        self.__sourceimage__ = None
        self.__condition__ = None
    
    def __del__(self):
        del self.__result__
        del self.__sourceimage__
        del self.__condition__

    def getResult(self):
        return self.__result__
    
    def setResult(self, value):
        self.__result__ = value
    
    def getSourceImage(self):
        return self.__sourceimage__
    
    def setSourceImage(self, value):
        self.__sourceimage__ = value
    
    def getCondition(self):
        return self.__condition__
    
    def setCondition(self, value):
        self.__condition__ = value