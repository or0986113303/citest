import serial
import numpy as np
from Model import Ammeter

class Control(object):
    def __init__(self):
        self.__model__ = None
        self.__serial__ = serial.Serial()
    
    def __del__(self):
        del self.__model__
        if self.__serial__.is_open:
            self.__serial__.close()
        del self.__serial__
    
    def getThershold(self, key):
        return self.__model__.getThershold(key)
    
    def setThershold(self, value):
        self.__model__.setThershold(value)
    
    def checkAmmeterValue(self):
        value = self.readvalue()
        unit = self.getunit()
        graduatio = self.getgraduation()

        if value <= float(getThershold("uppervalue")) and \
        value <= float(getThershold("lowervalue")) and \
        unit == getThershold("unit") and \
        graduatio == getThershold("graduatio"):
            result = {"Power" : {"items" : graduatio + unit, "testvalue" : value, "testresult" : True}}
        else : 
            result = {"Power" : {"items" : graduatio + unit, "testvalue" : value, "testresult" : False}}

        '''
        if value <= getThershold("value") and \
        unit == getThershold("unit") and \
        graduatio == getThershold("graduatio"):
            result = {"Power" : {"items" : graduatio + unit, "testvalue" : value, "testresult" : True}}
        else :
            result = {"Power" : {"items" : graduatio + unit, "testvalue" : value, "testresult" : False}}
        return result
        '''

    def __portIsUsable__(self):
        try:
            self.__serial__.close()
            self.__serial__.open()
            return True
        except:
            return False
        
    def __mappingtable__(self, map1, map2, first) :
        valuestring = ""
        combinetmp = ""
        if first :
            data = map1[3] + map1[2] + map1[1] + map2[4] + map2[3] + map2[2] + map2[1]
            #print "first"
            #print data
            tmp = self.__model__.reducetable[data]
            if map1[4] == "0" : 
                combinetmp += tmp
            else :
                combinetmp = "-"
                combinetmp += tmp
        else :
            data = map1[3] + map1[2] + map1[1] + map2[4] + map2[3] + map2[2] + map2[1]
            
            #print "other"
            #print map1
            #print map2
            #print data
            tmp = self.__model__.reducetable[data]
            if map1[4] == "0" : 
                combinetmp += tmp
            else :
                combinetmp = "."
                combinetmp += tmp

        valuestring = combinetmp
        return valuestring

    def __reducevalue__(self) :
        result = ""
        if self.__model__.getType() == "GDM-396" :
            #print self.__model__.ledtable[1]
            firstchr = self.__mappingtable__(self.__model__.ledtable[2], self.__model__.ledtable[3], first = True)
            #print "firstchr"
            #print firstchr
            secendchr = self.__mappingtable__(self.__model__.ledtable[4], self.__model__.ledtable[5], first = False)
            #print "secendchr"
            #print secendchr
            thirdchr = self.__mappingtable__(self.__model__.ledtable[6], self.__model__.ledtable[7], first = False)
            #print "thirdchr"
            #print thirdchr
            fourthchr = self.__mappingtable__(self.__model__.ledtable[8], self.__model__.ledtable[9], first = False)
            #print "fourthchr"
            #print fourthchr
            result = firstchr + secendchr + thirdchr + fourthchr
        else :
            if ord(self.__model__.feedbacktmp[6]) == 49 :
                self.__model__.data = self.__model__.valuetmp[:1] + "." + self.__model__.valuetmp[1:]
            elif ord(self.__model__.feedbacktmp[6]) == 50 :
                self.__model__.data = self.__model__.valuetmp[:2] + "." + self.__model__.valuetmp[2:]
            elif ord(self.__model__.feedbacktmp[6]) == 52 :
                self.__model__.data = self.__model__.valuetmp[:3] + "." + self.__model__.valuetmp[3:]
            elif ord(self.__model__.feedbacktmp[6]) == 48 :
                self.__model__.data = self.__model__.valuetmp[:1] + "." + self.__model__.valuetmp[1:]
            elif ord(self.__model__.feedbacktmp[6]) == 51 :
                self.__model__.data = self.__model__.valuetmp[:3] + "." + self.__model__.valuetmp[3:]
            else :
                self.__model__.data = self.__model__.valuetmp
            #print result
            if ord(self.__model__.data[0]) == 63 or ord(self.__model__.data[0]) == 50:
                #print self.__model__.data[0]
                self.__model__.data = "0.000"
            else :
                #print ord(self.__model__.data[0])
                self.__model__.data = self.__model__.data

            self.__model__.unit = self.__model__.feedbacktmp[10]
            self.__model__.graduation = self.__model__.feedbacktmp[9]
            
            result = self.__model__.data
        
        return result

    def getgraduation(self) :
        graduation = ""
        if self.__model__.getType() == "GDM-396" :
            if self.__model__.ledtable[11][4] == "1" :
                graduation = "m"
            elif self.__model__.ledtable[11][2] == "1" :
                graduation = "M"
            elif self.__model__.ledtable[10][2] == "1" :
                graduation = "k"
            elif self.__model__.ledtable[10][3] == "1" :
                graduation = "n"
            elif self.__model__.ledtable[10][4] == "1" :
                graduation = "u"
        else :
            graduation = self.__model__.graduationlookuptable[bin(ord(self.__model__.graduation))]
        
        self.__model__.result["graduation"] = graduation
        return self.__model__.result["graduation"]
        
    def getunit(self) :
        unit = ""
        if self.__model__.getType() == "GDM-396" :
            if self.__model__.ledtable[13][4] == "1" :
                unit = "A"
            elif self.__model__.ledtable[13][3] == "1" :
                unit = "V"
        else :
            unit = self.__model__.unitlookuptable[bin(ord(self.__model__.unit))]
        
        self.__model__.result["unit"] = unit
        return self.__model__.result["unit"]
        
    def readvalue(self) :
        feedbackstring = ""
        feedbackstring = self.__readfeedback__()
        value = ""
        if self.__model__.getType() == "GDM-396" :
            for i in range(0,self.__model__.getLength(),1) :
                #print ord(feedbackstring[i])
                data = bin(ord(feedbackstring[i])%16)
                for j in range(1,5,1) :
                    self.__model__.ledtable[i + 1][j] = "0"
                if len(data) == 5 :
                    for j in range(1,4,1) :
                        self.__model__.ledtable[i + 1][j] = "0"
                        self.__model__.ledtable[i + 1][j] = data[len(data) - j]
                elif len(data) == 6 :
                    for j in range(1,5,1) :
                        self.__model__.ledtable[i + 1][j] = "0"
                        self.__model__.ledtable[i + 1][j] = data[len(data) - j]
                elif len(data) == 4 :
                    for j in range(1,3,1) :
                        self.__model__.ledtable[i + 1][j] = "0"
                        self.__model__.ledtable[i + 1][j] = data[len(data) - j]
                elif len(data) == 3 :
                    self.__model__.ledtable[i + 1][j] = "0"
                    self.__model__.ledtable[i + 1][1] = data[2]

            value = self.__reducevalue__()
        else :
            self.__model__.valuetmp = feedbackstring[1:5]
            self.__model__.feedbacktmp = feedbackstring
            value = self.__reducevalue__()
            
        
        self.__model__.result["value"] = float(value)
        return self.__model__.result["value"]
        

    def __readfeedback__(self):
        feedbackstring = ""
        keeprun = True
        keepread = True
        #feedbackstring = self.__serial__.read(self.__model__.getLength())
        count = 0
        if self.__model__.getType() == "GDM-396" :
            while keeprun:
                tmp = self.__serial__.read()
                if tmp == '\x17' :
                    while keepread :
                        feedbackstring += tmp
                        tmp = self.__serial__.read()
                        count += 1
                        if count == self.__model__.getLength() and feedbackstring[0] == "\x17" :
                            keeprun = False
                            keepread = False
                            break
        else :
            while keeprun:
                tmp = self.__serial__.read()
                if tmp == "+" :
                    while keepread :
                        feedbackstring += tmp
                        tmp = self.__serial__.read()
                        count += 1
                        if count == self.__model__.getLength() and feedbackstring[0] == "+" :
                            keeprun = False
                            keepread = False
                            break
        
        #print "run counter : "
        #print count2
        return feedbackstring
        
    def connect(self, comport = "COM1", baudrate = 2400, type = "GDM-396") :
        if self.__model__== None:
            self.__model__ = Ammeter.Model(comport, baudrate, type)
        
        if not self.__serial__.is_open :
            self.__serial__.port = self.__model__.getPort()
            self.__serial__.baudrate = self.__model__.getBaudrate()
            self.__serial__.timeout = 1
            self.__serial__.bytesize = self.__model__.getBytesize()
            self.__serial__.parity = self.__model__.getParity()
            #print self.__serial__

        result = self.__portIsUsable__()
        #print result
        return result
    
    def disconnect(self):
        result = False
        if self.__serial__.is_open :
            self.__serial__.close()
            if self.__serial__.is_open :
                result = True
            else :
                result = False
        else :
            result = True
        return result
            
            
