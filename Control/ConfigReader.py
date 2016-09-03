import ConfigParser
import os, fnmatch

from Model import ParameterList

class Control(object):
    def __init__(self, path):
        self.__reader__ = ConfigParser.ConfigParser()
        self.__reader__.optionxform = str
        try :
            #print self.__find__('settings.ini', path)[0].split('[')[0].split(']')[0]
            self.__filename__ = self.__find__('settings.ini', path)[0].split('[')[0].split(']')[0]
            self.__reader__.read(self.__filename__)
            self.__datarender__()
            self.isSuccess = True
        except :
            self.isSuccess = False
    
    def __del__(self):
        del self.__reader__
        del self.__filename__

    def __find__(self, pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result
    
    def __datarender__(self):
        for item in self.__reader__.items(ParameterList.FW):
            ParameterList.FWVERSIONCHECK[item[0]] = item[1]

        for item in self.__reader__.items(ParameterList.CROSSCENTER):
            ParameterList.SHIFTTHERSHOLD[item[0]] = item[1]
        
        for item in self.__reader__.items(ParameterList.COLORCHECK):
            ParameterList.COLORCONDITION[item[0]] = item[1]
        
        for item in self.__reader__.items(ParameterList.AMMETERSELECT):
            ParameterList.AMMETERTHERSHOLD[item[0]] = item[1]

        for item in self.__reader__.items(ParameterList.STATION):
            if item[0] == ParameterList.LENGTH : 
                ParameterList.SERIEALLENGTH = int(item[1])
            else :
                ParameterList.WORKINGSTATION[item[0]] = item[1]
        
        for item in self.__reader__.items(ParameterList.MTF):
            ParameterList.MTFTHERSHOLD[item[0]] = item[1]
        
        for item in self.__reader__.items(ParameterList.SENSOR):
            ParameterList.SENSORPIXELSCALE[item[0]] = float(item[1])
        
        for item in self.__reader__.items(ParameterList.LINE):
            ParameterList.LINEINFORMATION[item[0]] = item[1]

        for item in self.__reader__.items(ParameterList.HW):
            if item[0] == ParameterList.PARTICLE :
                ParameterList.FFTTHERSHOLD = int(item[1])
                #print ParameterList.FFTTHERSHOLD
            elif item[0] == ParameterList.CAMERAIDSTRING :
                ParameterList.CAMERAID = int(item[1])
                #print ParameterList.CAMERAID
            elif item[0] == ParameterList.LIGHTLEVEL :
                ParameterList.LIGHTVALUE = int(item[1])
            else :
                ParameterList.CONFIGURE[item[0]] = item[1]
    