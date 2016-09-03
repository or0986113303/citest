import serial
#import numpy as np
from Model import Arduino
class Control(object):
    def __init__(self):
        self.__model__ = None
        self.__serial__ = serial.Serial()
        self.__binaryfilebuffer__ = None
        self.__filelength__ = None
    
    def __del__(self):
        del self.__model__
        if self.__serial__.is_open:
            self.__serial__.close()
        del self.__serial__
    
    def __portIsUsable__(self):
        try:
            self.__serial__.close()
            self.__serial__.open()
            return True
        except:
            return False

    def connect(self, port, baudrate):
        self.__model__ = Arduino.Model(port, baudrate)
        self.__serial__.baudrate = self.__model__.getbaudrate()
        self.__serial__.port = self.__model__.getport()
        self.__serial__.timeout = 1
        if self.__portIsUsable__() :
            return True
        else : 
            return False
        
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

    def __startsend__(self):
        self.__binaryfilebuffer__ = self.__model__.getbinaryfile()
        self.__filelength__ = self.__lengthparser__(len(self.__binaryfilebuffer__))
        startcommand = "DATA_0000_0000_" + self.__filelength__ + "_##"
        #print startcommand
        try :
            self.__serial__.write(self.__model__.commandlist["startsend"])
            return True
        except:
            return False

    def __i2cread__(self):
        try :
            self.__serial__.write(self.__model__.commandlist["i2cread"])
            return True
        except:
            return False
    
    def checkfwversion(self):
        
        feedbackstring = ""
        checkresult = False
        while not (feedbackstring.find("MCU_STATUS_04##") > 1 \
            or feedbackstring.find("MCU_STATUS_10##") > 1 \
            or feedbackstring.find("MCU_STATUS_09##") > 1 \
            or feedbackstring == self.__model__.gettimeoutcondition()):
            self.__i2cread__()
            feedbackstring = self.__readfeedback__()
        #print feedbackstring
        if feedbackstring == self.__model__.gettimeoutcondition() :
            checkresult = False
        
        if feedbackstring.find("MCU_STATUS_09##") > 1:
            checkresult = True
        else :
            checkresult = False
            
        if feedbackstring.find("MCU_STATUS_04##") > 1:
            checkresult = True
        else :
            checkresult = False
        
        return checkresult

    def i2cscan(self):
        try :
            self.__serial__.write(self.__model__.commandlist["i2cscan"])
            return True
        except:
            return False
    
    def __eepromwrite__(self):
        try :
            self.__serial__.write(self.__model__.commandlist["eepromwrite"])
            return True
        except:
            return False
    
    def finish(self):
        try :
            self.__serial__.write(self.__model__.commandlist["finish"])
            return True
        except:
            return False

    def __sendcommand__(self, command):
        self.__serial__.write(command)
        #self.__serial__.flushOutput()
    
    def __lengthparser__(self, length):
        
        currentlength = None
        #print length
        if length < 10 :
            currentlength = "000" + str(length)
        if length >= 10 and length < 100 :
            currentlength = "00" + str(length)
        if length >= 100 and length < 1000 :
            currentlength = "0" + str(length)
        if length >= 1000 and length < 10000 :
            currentlength = str(length)
        return currentlength

    def sendbinaryfile(self):
        keepsend = True
        startcounter = 0
        currentlength = None
        checkresult = False
        self.__binaryfilebuffer__ = self.__model__.getbinaryfile()
        while keepsend:
            currentlength = self.__lengthparser__(startcounter)
            #print currentlength
            #print len(self.__binaryfilebuffer__)
            #print startcounter + 2
            if startcounter + 2 == len(self.__binaryfilebuffer__) :
                #print "1"
                binaryfiletmp = "DATA_" + str(self.__binaryfilebuffer__[startcounter]) \
                + str(self.__binaryfilebuffer__[startcounter+1]) + chr(255) \
                + chr(255) + "_" + currentlength + "_" + self.__filelength__ + "_##"
            elif startcounter + 3 == len(self.__binaryfilebuffer__) :
                #print "2"
                binaryfiletmp = "DATA_" + str(self.__binaryfilebuffer__[startcounter]) \
                + str(self.__binaryfilebuffer__[startcounter+1]) + str(self.__binaryfilebuffer__[startcounter+2]) \
                + chr(255) + "_" + currentlength + "_" + self.__filelength__ + "_##"
            else :
                binaryfiletmp = "DATA_" + str(self.__binaryfilebuffer__[startcounter]) \
                + str(self.__binaryfilebuffer__[startcounter+1]) + str(self.__binaryfilebuffer__[startcounter+2]) \
                + str(self.__binaryfilebuffer__[startcounter+3]) + "_" + currentlength + "_" + self.__filelength__ + "_##"
            
            #print binaryfiletmp
            feedbackstring = ""
            while not (feedbackstring.find("MCU_STATUS_00##") > 1 \
            or feedbackstring.find("MCU_STATUS_01##") > 1 \
            or feedbackstring.find("MCU_STATUS_02##") > 1 \
            or feedbackstring == self.__model__.gettimeoutcondition()):
                try :
                    self.__serial__.write(binaryfiletmp)
                except:
                    keepsend = False
                    checkresult = False
                    #print "except"
                    break
                feedbackstring = self.__readfeedback__()
                #print feedbackstring
                #print "get : " + feedbackstring
             
            if feedbackstring == self.__model__.gettimeoutcondition() :
                #print feedbackstring
                #print self.__model__.gettimeoutcondition()
                keepsend = False
                checkresult = False
                break
            #print len(self.__binaryfilebuffer__) - 4
            #print startcounter
            if startcounter >= len(self.__binaryfilebuffer__) - 4 :
                keepsend = False
                checkresult = True
                #print "break point"
            startcounter += self.__model__.getbinaryfilebufferlength()
        return checkresult
        #self.__serial__.write(file)
    
    def checkwriteeeprom(self):
        feedbackstring = ""
        checkresult = False
        while not (feedbackstring.find("MCU_STATUS_03##") > 1 \
        or feedbackstring.find("MCU_STATUS_09##") > 1  \
        or feedbackstring == self.__model__.gettimeoutcondition()):
            self.__eepromwrite__()
            feedbackstring = self.__readfeedback__()
        
        if feedbackstring == self.__model__.gettimeoutcondition() :
            checkresult = False

        if feedbackstring.find("MCU_STATUS_03##") > 1:
            checkresult = True
        else :
            checkresult = False

        return checkresult

    def checkcurrectstart(self):
        feedbackstring = ""
        checkresult = False
        while not (feedbackstring.find("MCU_STATUS_00##") > 1 \
            or feedbackstring.find("MCU_STATUS_09##") > 1 
            or feedbackstring == self.__model__.gettimeoutcondition()):
            self.__startsend__()
            feedbackstring = self.__readfeedback__()
        
        if feedbackstring == self.__model__.gettimeoutcondition() :
            checkresult = False

        if feedbackstring.find("MCU_STATUS_00##") > 1:
            checkresult = True
        else :
            checkresult = False
        
        return checkresult

    def __readfeedback__(self):
        feedbackstring = ""
        #print feedbackstring
        keepread = True
        retrycounter = 0
        #print keepread
        while keepread :
            tmp = ""
            tmp = self.__serial__.read()
            #print tmp
            feedbackstring += tmp
            #print len(tmp)
            #print feedbackstring
            #print feedbackstring.find("##")
            if feedbackstring.find("##") > 12 :
                keepread = False
                break
            if len(tmp) == 0:
                #print retrycounter
                retrycounter += 1
            if retrycounter >= self.__model__.getretrytimes() :
                keepsend = False
                feedbackstring = self.__model__.gettimeoutcondition()
                break
        #print feedbackstring
        return feedbackstring

    def readfeedback(self):
        return self.__readfeedback__()

    def getbinaryfile(self):
        return self.__model__.getbinaryfile()
    
    def setbinaryfile(self, value):
        self.__model__.setbinaryfile(value)
    
    #def savebinaryfile(self):
    def __searchXYShiftaddress__(self, FWFile):
        index = FWFile.find("\xfe\x30\02") + 3
        self.__model__.setIndex(index)

    def reduceXYshift(self, shiftvalue, shiftlimit, scaling):
        FWFile = self.__model__.getbinaryfile()
        self.__searchXYShiftaddress__(FWFile)
        #print scaling["XScale"]
        #print scaling["YScale"]
        if shiftvalue["XShift"] > int(shiftlimit["XShift"]):
            FWFile = FWFile[:self.__model__.indexlist["XHigh"]] + chr(int("0x00",16)) + FWFile[self.__model__.indexlist["XHigh"] + 1:]
            FWFile = FWFile[:self.__model__.indexlist["XLower"]] + chr(int("0x0C",16)) + FWFile[self.__model__.indexlist["XLower"] + 1:]
            #FWFile.replace(FWFile[563] ,chr(int("0x00",16)))
            #FWFile.replace(FWFile[565] ,chr(int("0x06",16)))
        else : 
            if shiftvalue["XShift"] < - int(shiftlimit["XShift"]):
                FWFile = FWFile[:self.__model__.indexlist["XHigh"]] + chr(int("0x03",16)) + FWFile[self.__model__.indexlist["XHigh"] + 1:]
                FWFile = FWFile[:self.__model__.indexlist["XLower"]] + chr(int("0xF3",16)) + FWFile[self.__model__.indexlist["XLower"] + 1:]
                #FWFile.replace(FWFile[563] ,chr(int("0x01",16)))
                #FWFile.replace(FWFile[565] ,chr(int("0x06",16)))
            else:
                if shiftvalue["XShift"] > 0:
                    FWFile = FWFile[:self.__model__.indexlist["XHigh"]] + chr(int("0x00",16)) + FWFile[self.__model__.indexlist["XHigh"] + 1:]
                    ##FWFile = FWFile[:565] + chr(int("0x00",16)) + FWFile[566:]
                    FWFile = FWFile[:self.__model__.indexlist["XLower"]] + chr(int(abs(np.round(shiftvalue["XShift"]*scaling["XScale"])))) + FWFile[self.__model__.indexlist["XLower"] + 1:]
                    #FWFile.replace(FWFile[563] ,chr(int("0x00",16)))
                    #FWFile.replace(FWFile[565] ,chr(int(abs(np.round(shiftvalue["X"])))))
                else : 
                    FWFile = FWFile[:self.__model__.indexlist["XHigh"]] + chr(int("0x03",16)) + FWFile[self.__model__.indexlist["XHigh"] + 1:]
                    ##FWFile = FWFile[:565] + chr(int("0xFF",16)) + FWFile[566:]
                    FWFile = FWFile[:self.__model__.indexlist["XLower"]] + chr(255 - int(abs(np.round(shiftvalue["XShift"]*scaling["XScale"])))) + FWFile[self.__model__.indexlist["XLower"] + 1:]
                    #FWFile.replace(FWFile[563] ,chr(int(0x01,16)))
                    #FWFile.replace(FWFile[565] ,chr(int(abs(np.round(shiftvalue["X"])))))
                    
                
            
        if shiftvalue["YShift"] > int(shiftlimit["YShift"]):
            FWFile = FWFile[:self.__model__.indexlist["YHigh"]] + chr(int("0x00",16)) + FWFile[self.__model__.indexlist["YHigh"] + 1:]
            FWFile = FWFile[:self.__model__.indexlist["YLower"]] + chr(int("0x0C",16)) + FWFile[self.__model__.indexlist["YLower"] + 1:]
            #FWFile.replace(FWFile[567] ,chr(int("0x00",16)))
            #FWFile.replace(FWFile[569] ,chr(int("0x06",16)))
        else : 
            if shiftvalue["YShift"] < - int(shiftlimit["YShift"]) :
                FWFile = FWFile[:self.__model__.indexlist["YHigh"]] + chr(int("0x03",16)) + FWFile[self.__model__.indexlist["YHigh"] + 1:]
                FWFile = FWFile[:self.__model__.indexlist["YLower"]] + chr(int("0xF3",16)) + FWFile[self.__model__.indexlist["YLower"] + 1:]
                #FWFile.replace(FWFile[567] ,chr(int("0x01",16)))
                #FWFile.replace(FWFile[569] ,chr(int("0x06",16)))
            else :
                if shiftvalue["YShift"] > 0 :
                    FWFile = FWFile[:self.__model__.indexlist["YHigh"]] + chr(int("0x00",16)) + FWFile[self.__model__.indexlist["YHigh"] + 1:]
                    ##FWFile = FWFile[:569] + chr(int("0x00",16)) + FWFile[570:]
                    FWFile = FWFile[:self.__model__.indexlist["YLower"]] + chr(int(abs(np.round(shiftvalue["YShift"]*scaling["YScale"])))) + FWFile[self.__model__.indexlist["YLower"] + 1:]
                    #FWFile.replace(FWFile[567] ,chr(int("0x00",16)))
                    #FWFile.replace(FWFile[569] ,chr(int(abs(np.round(shiftvalue["Y"])))))
                else :
                    FWFile = FWFile[:self.__model__.indexlist["YHigh"]] + chr(int("0x03",16)) + FWFile[self.__model__.indexlist["YHigh"] + 1:]
                    ##FWFile = FWFile[:569] + chr(int("0xFF",16)) + FWFile[570:]
                    FWFile = FWFile[:self.__model__.indexlist["YLower"]] + chr(255 - int(abs(np.round(shiftvalue["YShift"]*scaling["YScale"])))) + FWFile[self.__model__.indexlist["YLower"] + 1:]
                    #FWFile.replace(FWFile[567] ,chr(int("0x01",16)))
                    #FWFile.replace(FWFile[569] ,chr(int(abs(np.round(shiftvalue["Y"])))))

        self.setbinaryfile(FWFile)

    def recaculatechecksum(self):
        FWFile = self.__model__.getbinaryfile()
        tmp = 0x00
        for i in range(0,len(FWFile)):
            if not i == 4:
                tmp += ord(FWFile[i])
            '''
            else :
                print FWFile[i]
                print ord(FWFile[i])
            '''
        invercechecksum = 65536
        hexresult = hex(invercechecksum - tmp)
        result = '0x' + hexresult[4] + hexresult[5]
        FWFile = FWFile[:4] + chr(int(result,16)) + FWFile[5:]
        
        self.setbinaryfile(FWFile)
        
    
        