class Model(object):
    def __init__(self, port, baudrate):
        self.__port__ = port
        self.__baudrate__ = baudrate
        self.__binaryfile__ = None
        self.commandlist = {"startsend":"DATA_0000_0000_0008_##", \
        "i2cscan":"I2CS_0000_0000_0000_##" , \
        "eepromwrite":"I2CW_0000_0000_0000_##", \
        "finish":"I2CW_0000_0000_0000_##", \
        "i2cread" : "I2CR_3116_0000_0000_##"}
        self.__binarybufferlenght__ = 4
        self.__retrytimes__ = 4
        self.__timeoutstatus__ = "TimeOut"
        self.__index__ = 0
        self.indexlist = None#{"XHigh" : self.__index__, "XLower" : self.__index__ + 2, "YHigh" : self.__index__ + 4, "YLower" : self.__index__ + 6}
    
    def __del__(self):
        del self.__port__
        del self.__baudrate__
        del self.__binaryfile__
        del self.__binarybufferlenght__
        del self.commandlist
        del self.__index__
        del self.indexlist
        
    def getIndex(self):
        return self.__index__
    
    def setIndex(self, value):
        self.__index__ = value
        self.indexlist = {"XHigh" : self.__index__, "XLower" : self.__index__ + 2, "YHigh" : self.__index__ + 4, "YLower" : self.__index__ + 6}
    
    def gettimeoutcondition(self):
        return self.__timeoutstatus__

    def getretrytimes(self):
        return self.__retrytimes__

    def getport(self):
        return self.__port__
    
    def setport(self, value):
        self.__port__ = value

    def getbaudrate(self):
        return self.__baudrate__
    
    def setbaudrate(self, value):
        self.__baudrate__ = value
    
    def getbinaryfile(self):
        return self.__binaryfile__
    
    def setbinaryfile(self, value):
        self.__binaryfile__ = value
    
    def getbinaryfilebufferlength(self):
        return self.__binarybufferlenght__
    
        