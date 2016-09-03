import serial
from Model import Lighter

class Control(object):
    def __init__(self, parameter = None):
        self.__model__ = None
        #if self.__model__== None:
        #    self.__model__ = Lighter.Model(parameter = parameter)
        self.__items__ = {"lightfirst" : None, "lightsecend" : None, "lightthird" : None}
        self.__serial__ = {"lightfirst" : None, "lightsecend" : None, "lightthird" : None}
        self.__serial__["lightfirst"] = serial.Serial()
        self.__serial__["lightsecend"] = serial.Serial()
        self.__serial__["lightthird"] = serial.Serial()
        
    
    def __del__(self):
        del self.__model__
        for majorkey, subdict in self.__items__.iteritems():
            if self.__serial__[majorkey].is_open:
                self.__serial__[majorkey].close()
        del self.__serial__
    
    def __portIsUsable__(self, key):
        try:
            self.__serial__[key].close()
            self.__serial__[key].open()
            return True
        except:
            return False
    
    def connect(self, parameter) :
        result = 0
        if self.__model__== None:
            self.__model__ = Lighter.Model(parameter = parameter)

        for majorkey, subdict in self.__items__.iteritems():
            if not self.__serial__[majorkey].is_open :
                if majorkey == "lightfirst" :
                    self.__serial__[majorkey].port = self.__model__.lightparameter[majorkey]["Lighter1Port"]
                    self.__serial__[majorkey].baudrate = self.__model__.lightparameter[majorkey]["Lighter1BaudRate"]
                    self.__serial__[majorkey].timeout = 1
                    self.__serial__[majorkey].bytesize = 8
                    self.__serial__[majorkey].parity = "N"
                elif majorkey == "lightsecend" :
                    self.__serial__[majorkey].port = self.__model__.lightparameter[majorkey]["Lighter2Port"]
                    self.__serial__[majorkey].baudrate = self.__model__.lightparameter[majorkey]["Lighter2BaudRate"]
                    self.__serial__[majorkey].timeout = 1
                    self.__serial__[majorkey].bytesize = 8
                    self.__serial__[majorkey].parity = "N"
                elif majorkey == "lightthird" :
                    self.__serial__[majorkey].port = self.__model__.lightparameter[majorkey]["Lighter3Port"]
                    self.__serial__[majorkey].baudrate = self.__model__.lightparameter[majorkey]["Lighter3BaudRate"]
                    self.__serial__[majorkey].timeout = 1
                    self.__serial__[majorkey].bytesize = 8
                    self.__serial__[majorkey].parity = "N"

            if self.__portIsUsable__(majorkey) :
                result += 1

        #print result
        return result
    
    def disconnect(self):
        result = 0
        for majorkey, subdict in self.__items__.iteritems():
            self.__serial__[majorkey].close()
            if not self.__serial__[majorkey].is_open :
                result += 1
        return result
    
    def setLightValue(self, value):
        for majorkey, subdict in self.__items__.iteritems():
            self.__model__.leightvalue[majorkey]["value"] = value
        
        for majorkey, subdict in self.__items__.iteritems():
            if len(self.__model__.leightvalue[majorkey]) < 2 :
                self.__serial__[majorkey].write("0" + str(self.__model__.leightvalue[majorkey]) + "\n")
            else :
                self.__serial__[majorkey].write(str(self.__model__.leightvalue[majorkey]) + "\n")
                

        
        
