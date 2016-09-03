class Model(object):
    def __init__(self, port, baudrate, type):
        self.__port__ = port
        self.__baudrate__ = baudrate
        self.__type__ = type
        self.__length__ = 14
        self.__thershold__ = None
        self.result = {"value" : 0, "unit" : "unknow", "graduation" : "unknow"}
        if self.__type__ == "GDM-396" :
            
            self.__bytesize__ = 7
            self.__parity__ = "O"
            self.byte1 = {1 : '0', 2 : '0', 3 : '0', 4 : '0'}
            self.byte2 = {1 : '0', 2 : '0', 3 : '0', 4 : '0'}
            self.byte3 = {1 : '0', 2 : '0', 3 : '0', 4 : '0'}
            self.byte4 = {1 : '0', 2 : '0', 3 : '0', 4 : '0'}
            self.byte5 = {1 : '0', 2 : '0', 3 : '0', 4 : '0'}
            self.byte6 = {1 : '0', 2 : '0', 3 : '0', 4 : '0'}
            self.byte7 = {1 : '0', 2 : '0', 3 : '0', 4 : '0'}
            self.byte8 = {1 : '0', 2 : '0', 3 : '0', 4 : '0'}
            self.byte9 = {1 : '0', 2 : '0', 3 : '0', 4 : '0'}
            self.byte10 = {1 : '0', 2 : '0', 3 : '0', 4 : '0'}
            self.byte11 = {1 : '0', 2 : '0', 3 : '0', 4 : '0'}
            self.byte12 = {1 : '0', 2 : '0', 3 : '0', 4 : '0'}
            self.byte13 = {1 : '0', 2 : '0', 3 : '0', 4 : '0'}
            self.byte14 = {1 : '0', 2 : '0', 3 : '0', 4 : '0'}
            self.ledtable = {1 : self.byte1, 2 : self.byte2, 3 : self.byte3, \
            4 : self.byte4, 5 : self.byte5, 6 : self.byte6, 7 : self.byte7, 8 : self.byte8, \
            9 : self.byte9, 10 : self.byte10, 11 : self.byte11, 12 : self.byte12, 13 : self.byte13, 14 : self.byte14}

            self.reducetable = {"1111101" : "0", "0000101" : "1", "1011011" : "2", "0011111" : "3", "0100111" : "4",\
            "0111110" : "5", "1111110" : "6", "0110101" : "7", "1111111" : "8", "0111111" : "9", \
            "0001101" : "1", "0101000" : "5", "1101101" : "3", "0101111" : "4", "0000100" : "9", "0010101" : "7", "0001111" : "6", "0011101" : "7", "1101111" : "3",\
            "1001100" : "6", "0100100" : "7", "0101101" : "7", "1110111" : "5", "0001000" : "3", "1111100" : "0", "0000111" : "1", "1011100" : "2", "0000000" : "1"}
        else :
            self.valuetmp = None
            self.feedbacktmp = None
            self.data = None
            self.unit = None
            self.graduation = None
            self.unitlookuptable = {"0b10000000" : "V", "0b1000000" : "A", "0b1000" : "Hz", "0b100000" : "Omu", "0b10" : "hFE"}
            self.graduationlookuptable = {"0b0" : "", "0b1000000" : "m", "0b10000000" : "u", "0b10000" : "M", "0b100000" : "k"}
            self.__bytesize__ = 8
            self.__parity__ = "N"

        
    
    def __del__(self):
        del self.__port__
        del self.__baudrate__
        del self.__length__ 
        del self.__thershold__
        if self.__type__ == "GDM-396" :
            del self.ledtable
            del self.byte1
            del self.byte2
            del self.byte3
            del self.byte4
            del self.byte5
            del self.byte6
            del self.byte7
            del self.byte8
            del self.byte9
            del self.byte10
            del self.byte11
            del self.byte12
            del self.byte13
            del self.byte14
        else :
            del self.valuetmp
            del self.data
            del self.unit
            del self.graduation
            del self.unitlookuptable
            del self.graduationlookuptable
        
        del self.__bytesize__
        del self.__parity__
        del self.__type__
    
    def getThershold(self, key):
        return self.__thershold__[key]
    
    def setThershold(self, value):
        self.__thershold__ = value

    def getBytesize(self) :
        return self.__bytesize__
    
    def setBytesize(self, value) :
        self.__bytesize__ = value
    
    def setParity(self, value) : 
        self.__parity__ = value

    def getParity(self) :
        return self.__parity__

    def getPort(self) :
        return self.__port__
    
    def setPort(self, value):
        self.__port__ = value
    
    def getBaudrate(self):
        return self.__baudrate__

    def setBaudrate(self, value):
        self.__baudrate__ = value

    def setType(self, value):
        self.__type__ = value
    
    def getType(self):
        return self.__type__
    
    def getLength(self):
        return self.__length__
    
    def setLength(self, value):
        self.__length__ = value