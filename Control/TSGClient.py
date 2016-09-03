from ctypes import *
from ctypes.wintypes import *
import ctypes
import os
import sys

from Model import ParameterList
from Model import TSGClient
#BuildRelease = True
class Control(object):
    def __init__(self):
        #if BuildRelease :
        self.__TGSlib__ = ctypes.WinDLL('SajetConnect.dll')
        #else : 
        #    self.__TGSlib__ = ctypes.WinDLL('D:/SW/Code/Camera/Python/mtf/SajetConnect.dll')

        self.__TGSlib__.SajetTransStart.argtypes = []
        self.__TGSlib__.SajetTransStart.restype = c_bool
        self.__TGSlib__.SajetTransData.argtypes = [c_int,c_char_p,POINTER(c_int)]
        self.__TGSlib__.SajetTransData.restype = c_bool
        self.__TGSlib__.SajetTransClose.argtypes = []
        self.__TGSlib__.SajetTransClose.restype = c_bool
        self.__messagelen__ = c_int()
        self.__message__ = c_char_p()
        self.__commandid__ = c_int()
        self.__commandlist__ = {"CMD_1":1, "CMD_2":2, "CMD_3":3, "CMD_5":5}
        self.__errorcode__ = None
        self.__model__ = TSGClient.Model()
        
    
    def __del__(self):
        del self.__TGSlib__
    
    def getresultdata(self):
        return self.__model__.getresultdata()

    def setresultdata(self, value):
        self.__model__.setresultdata(value)

    def getstation(self):
        return self.__model__.getstation()
    
    def setstation(self, value):
        self.__model__.setstation(value)
    
    def getemployeeID(self):
        return self.__model__.getemployeeID()
    
    def setemployeeID(self, value):
        self.__model__.setemployeeID(value)

    def getseriealnumber(self):
        return self.__model__.getseriealnumber()
    
    def setseriealnumber(self, value):
        self.__model__.setseriealnumber(value)

    def getcustomerseriealnumber(self):
        return self.__model__.getcustomerseriealnumber()
    
    def setcustomerseriealnumber(self, value):
        self.__model__.setcustomerseriealnumber(value)
    
    def getpassorfail(self):
        return self.__model__.getpassorfail()
    
    def setpassorfail(self, value):
        self.__model__.setpassorfail(value)

    def Connect(self):
        result = self.__TGSlib__.SajetTransStart()
        return result


    def DisConnect(self):
        result = self.__TGSlib__.SajetTransClose()
        return result
    
    def __checkfeedback__(self, value):
        data = {"result" : False, "message" : "NG", "errorcode" : "unknow"}
        if value[0:2] == ParameterList.OK :
            data["result"] = True
            data["message"] = "OK"
            data["errorcode"] = "unknow"
        else :
            data["result"] = False
            data["message"] = "NG"
            data["errorcode"] = value[3:8]
        return data
            

    def CheckStationAndEmployeeID(self):
        #print self.__model__.getstation()
        #print self.__model__.getemployeeID()
        self.__message__.value = self.__model__.getstation() + ";" \
        + self.__model__.getemployeeID() + ";"
        self.__commandid__.value = self.__commandlist__['CMD_1']
        self.__messagelen__.value = len(self.__message__.value)
        data = self.__TGSlib__.SajetTransData(self.__commandid__, self.__message__, byref(self.__messagelen__))
        return self.__checkfeedback__(self.__message__.value)
    
    def CheckStationAndSeriealNumber(self):
        #print type(self.__model__)
        #print self.__model__.getstation()
        #print self.__model__.getseriealnumber()
        self.__message__.value = self.__model__.getstation() + ";" \
        + self.__model__.getseriealnumber() + ";"
        self.__commandid__.value = self.__commandlist__['CMD_2']
        self.__messagelen__.value = len(self.__message__.value)
        data = self.__TGSlib__.SajetTransData(self.__commandid__, self.__message__, byref(self.__messagelen__))
        return self.__checkfeedback__(self.__message__.value)
    
    def CheckPassOrFail(self):
        self.__message__.value = self.__model__.getstation() + ";" \
        + self.__model__.getemployeeID() + ";" \
        + self.__model__.getseriealnumber() + ";" \
        + self.__model__.getcustomerseriealnumber() + ";" \
        + self.__model__.getpassorfail() + ";"
        self.__commandid__.value = self.__commandlist__['CMD_3']
        self.__messagelen__.value = len(self.__message__.value)
        self.__TGSlib__.SajetTransData(self.__commandid__, self.__message__, byref(self.__messagelen__))
        return self.__checkfeedback__(self.__message__.value)

    def CheckTestResult(self):
        self.__message__.value = self.__model__.getstation() + ";" \
        + self.__model__.getemployeeID() + ";" \
        + self.__model__.getseriealnumber() + ";" \
        + self.__model__.getresultdata()# + ";" 
        self.__commandid__.value = self.__commandlist__['CMD_5']
        self.__messagelen__.value = len(self.__message__.value)
        self.__TGSlib__.SajetTransData(self.__commandid__, self.__message__, byref(self.__messagelen__))
        #print self.__message__.value
        return self.__checkfeedback__(self.__message__.value)

    def clearnAmmeterResultForShopfloor(self, firstkey, secendkey, value):
        if secendkey == "testresult" :
            self.__model__.ammetercheckresultforshopfloor[firstkey][secendkey] = "FAIL"
        else :
            if secendkey == "testvalue" :
                self.__model__.ammetercheckresultforshopfloor[firstkey][secendkey] = "None"
            else :
                self.__model__.ammetercheckresultforshopfloor[firstkey][secendkey] = value
    
    def setAmmeterResultForShopfloor(self, firstkey, secendkey, value):
        #print value
        #print firstkey
        if secendkey == "testresult" :
            self.__model__.ammetercheckresultforshopfloor[firstkey][secendkey] = value[secendkey]
        else :
            if secendkey == "testvalue" :
                self.__model__.ammetercheckresultforshopfloor[firstkey][secendkey] = str(value[secendkey]) + value["items"] 
            else :
                self.__model__.ammetercheckresultforshopfloor[firstkey][secendkey] = value

    def __getAmmeterResultFromModelForShopfloor__(self, key):
        return self.__model__.ammetercheckresultforshopfloor[key]
    
    def clreanAmmeterResult(self):
        for majorkey, subdict in ParameterList.AMMETERCHECKRESULT.iteritems():
            self.clearnAmmeterResultForShopfloor(majorkey, ParameterList.ITEMS , \
            majorkey)
            self.clearnAmmeterResultForShopfloor(majorkey, ParameterList.TESTVALUE , \
            majorkey)
            self.clearnAmmeterResultForShopfloor(majorkey, ParameterList.TESTRESULT , \
            majorkey)
    
    def getAmmeterResult(self, value):
        for majorkey, subdict in ParameterList.AMMETERCHECKRESULT.iteritems():
            self.setAmmeterResultForShopfloor(majorkey, ParameterList.ITEMS, majorkey)
            self.setAmmeterResultForShopfloor(majorkey, ParameterList.TESTVALUE, value)
            self.setAmmeterResultForShopfloor(majorkey, ParameterList.TESTRESULT, value)
    
    def getAmmeterResultForShopfloor(self):
        arrangedata = ""
        for majorkey, subdict in ParameterList.AMMETERCHECKRESULT.iteritems():
            temp = self.__getAmmeterResultFromModelForShopfloor__(majorkey)
            #items = temp[ParameterList.ITEMS]
            #value = str(temp[ParameterList.TESTVALUE])
            #result = temp[ParameterList.TESTRESULT]
            #print temp
            if temp[ParameterList.ITEMS] == None :
                items = ParameterList.NONE
            else :
                items = temp[ParameterList.ITEMS]
            
            if temp[ParameterList.TESTVALUE] == None :
                value = ParameterList.NONE
            else :
                value = str(temp[ParameterList.TESTVALUE])
            
            if temp[ParameterList.TESTRESULT] == None :
                result = ParameterList.FAIL
            else :
                result = temp[ParameterList.TESTRESULT]

            arrangedata += items + ":" + value + ":" + result + ";"
        return arrangedata

    def clearnColorCheckResultForShopfloor(self, firstkey, secendkey, value):
        if secendkey == "testresult" :
            self.__model__.colorcheckresultforshopfloor[firstkey][secendkey] = "FAIL"
        else :
            if secendkey == "testvalue" :
                self.__model__.colorcheckresultforshopfloor[firstkey][secendkey] = "None"
            else :
                self.__model__.colorcheckresultforshopfloor[firstkey][secendkey] = value

    def setColorCheckResultForShopfloor(self, firstkey, secendkey, value):
        if secendkey == "testresult" :
            self.__model__.colorcheckresultforshopfloor[firstkey][secendkey] = value["Result"]
        else :
            if secendkey == "testvalue" :
                self.__model__.colorcheckresultforshopfloor[firstkey][secendkey] = value[firstkey]
            else :
                self.__model__.colorcheckresultforshopfloor[firstkey][secendkey] = value

    def getColorCheckResultForShopfloor(self, key):
        return self.__model__.colorcheckresultforshopfloor[key]
    
    def getColorCheckResult(self, value):
        for majorkey, subdict in ParameterList.COLORCHECKRESULT.iteritems():
            self.setColorCheckResultForShopfloor(majorkey, ParameterList.ITEMS, majorkey)
            self.setColorCheckResultForShopfloor(majorkey, ParameterList.TESTVALUE, value)
            self.setColorCheckResultForShopfloor(majorkey, ParameterList.TESTRESULT, value)
        #print self.__model__.colorcheckresultforshopfloor

    def clearnColorCheckResult(self):
        for majorkey, subdict in ParameterList.COLORCHECKRESULT.iteritems():
            self.clearnColorCheckResultForShopfloor(majorkey, ParameterList.ITEMS , \
            majorkey)
            self.clearnColorCheckResultForShopfloor(majorkey, ParameterList.TESTVALUE , \
            majorkey)
            self.clearnColorCheckResultForShopfloor(majorkey, ParameterList.TESTRESULT , \
            majorkey)

    def getColorCheckDataForSHopfloor(self):
        arrangedata = ""
        for majorkey, subdict in ParameterList.COLORCHECKRESULT.iteritems():
            temp = self.getColorCheckResultForShopfloor(majorkey)
            #print temp
            #print temp[ParameterList.ITEMS]
            #print str(temp[ParameterList.TESTVALUE])
            #print temp[ParameterList.TESTRESULT]

            if temp[ParameterList.ITEMS] == None :
                items = ParameterList.NONE
            else :
                items = temp[ParameterList.ITEMS]
            
            if temp[ParameterList.TESTVALUE] == None :
                value = ParameterList.NONE
            else :
                value = str(temp[ParameterList.TESTVALUE])
            
            if temp[ParameterList.TESTRESULT] == None :
                result = ParameterList.FAIL
            else :
                #print temp[ParameterList.TESTRESULT]
                if temp[ParameterList.TESTRESULT] == False or temp[ParameterList.TESTRESULT] == ParameterList.FAIL: 
                    result = ParameterList.FAIL
                else :
                    result = ParameterList.PASS
            #print items
            #print value
            #print result
            arrangedata += items + ":" + value + ":" + result + ";"
        
        return arrangedata

    def clearnFWCheckResultForShopfloor(self, firstkey, secendkey, value):
        #print self.__model__.fwcheckresultforshopfloor
        if secendkey == "testresult" :
            self.__model__.fwcheckresultforshopfloor[firstkey][secendkey] = "FAIL"
        else :
            if secendkey == "testvalue" :
                self.__model__.fwcheckresultforshopfloor[firstkey][secendkey] = "None"
            else :
                self.__model__.fwcheckresultforshopfloor[firstkey][secendkey] = value

    def getFWCheckResultForShopfloor(self, key):
        return self.__model__.fwcheckresultforshopfloor[key]

    def setFWCheckResultForShopfloor(self, firstkey, secendkey, value):
        if secendkey == "testresult" :
            self.__model__.fwcheckresultforshopfloor[firstkey][secendkey] = value
        else :
            if secendkey == "testvalue" :
                self.__model__.fwcheckresultforshopfloor[firstkey][secendkey] = value
            else :
                self.__model__.fwcheckresultforshopfloor[firstkey][secendkey] = value
    
    def clearnFWVersionCheckResult(self):
        for majorkey, subdict in ParameterList.FWVERSIONCHECK.iteritems():
            self.clearnFWCheckResultForShopfloor(majorkey, ParameterList.ITEMS , \
            majorkey)
            self.clearnFWCheckResultForShopfloor(majorkey, ParameterList.TESTVALUE , \
            majorkey)
            self.clearnFWCheckResultForShopfloor(majorkey, ParameterList.TESTRESULT , \
            majorkey)

    def getFWVersionCheckResult(self, value):
        for majorkey, subdict in ParameterList.FWVERSIONCHECK.iteritems():
            self.setFWCheckResultForShopfloor(majorkey, ParameterList.ITEMS, majorkey)
            if value :
                self.setFWCheckResultForShopfloor(majorkey, ParameterList.TESTVALUE, ParameterList.FWVERSIONCHECK[ParameterList.FWVERSION])
                self.setFWCheckResultForShopfloor(majorkey, ParameterList.TESTRESULT, ParameterList.PASS)
            else :
                self.setFWCheckResultForShopfloor(majorkey, ParameterList.TESTVALUE, "0.0.0")
                self.setFWCheckResultForShopfloor(majorkey, ParameterList.TESTRESULT, ParameterList.FAIL)

    def getFWVersionCheckResultForSHopfloor(self):
        arrangedata = ""
        for majorkey, subdict in ParameterList.FWVERSIONCHECK.iteritems():
            temp = self.getFWCheckResultForShopfloor(majorkey)
            #items = temp[ParameterList.ITEMS]
            #value = str(temp[ParameterList.TESTVALUE])
            #result = temp[ParameterList.TESTRESULT]
            if temp[ParameterList.ITEMS] == None :
                items = ParameterList.NONE
            else :
                items = temp[ParameterList.ITEMS]
            
            if temp[ParameterList.TESTVALUE] == None :
                value = ParameterList.NONE
            else :
                value = str(temp[ParameterList.TESTVALUE])
            
            if temp[ParameterList.TESTRESULT] == None :
                result = ParameterList.FAIL
            else :
                result = temp[ParameterList.TESTRESULT]

            arrangedata += items + ":" + value + ":" + result + ";"
        return arrangedata
    
    def clearnCrossCenterResultForShopfloor(self, firstkey, secendkey, value):
        if secendkey == "testresult" :
            self.__model__.crosscenterresultforshopfloor[firstkey][secendkey] = "FAIL"
        else :
            if secendkey == "testvalue" :
                self.__model__.crosscenterresultforshopfloor[firstkey][secendkey] = "None"
            else :
                self.__model__.crosscenterresultforshopfloor[firstkey][secendkey] = value

    def setCrossCenterResultForShopfloor(self, firstkey, secendkey, value, resultforui = None):
        if secendkey == "testresult" :
            #print self.__cameramodel__.crosscenterresultforshopfloor[firstkey]["testvalue"]
            #print value[firstkey]
            if abs(self.__model__.crosscenterresultforshopfloor[firstkey]["testvalue"]) <= int(value[firstkey]) :
                self.__model__.crosscenterresultforshopfloor[firstkey][secendkey] = "PASS"
                resultforui[firstkey] = "PASS"
            else :
                self.__model__.crosscenterresultforshopfloor[firstkey][secendkey] = "FAIL"
                resultforui[firstkey] = "FAIL"
        else :
            if secendkey == "testvalue" :
                self.__model__.crosscenterresultforshopfloor[firstkey][secendkey] = value[firstkey]
            else :
                #print value
                self.__model__.crosscenterresultforshopfloor[firstkey][secendkey] = value

    def getCrossCenterResultForShopfloor(self, key):
        return self.__model__.crosscenterresultforshopfloor[key]
    
    def clearnCrossCenterResult(self) :
        for majorkey, subdict in ParameterList.SHIFTTHERSHOLD.iteritems():
            #print majorkey
            self.clearnCrossCenterResultForShopfloor(majorkey, ParameterList.ITEMS , \
            majorkey)
            self.clearnCrossCenterResultForShopfloor(majorkey, ParameterList.TESTVALUE , \
            majorkey)
            self.clearnCrossCenterResultForShopfloor(majorkey, ParameterList.TESTRESULT , \
            majorkey)

    def getCrossCenterResult(self, shiftXYresult) :
        statuscounter = 0
        for majorkey, subdict in ParameterList.SHIFTTHERSHOLD.iteritems():
            #print majorkey
            self.setCrossCenterResultForShopfloor(majorkey, ParameterList.ITEMS, majorkey)
            self.setCrossCenterResultForShopfloor(majorkey, ParameterList.TESTVALUE, shiftXYresult)
            self.setCrossCenterResultForShopfloor(majorkey, ParameterList.TESTRESULT, ParameterList.SHIFTTHERSHOLD , ParameterList.SHIFTRESULT)
            if ParameterList.SHIFTRESULT[majorkey] == ParameterList.FAIL : 
                statuscounter +=1
            
        if statuscounter > 0 :
            return False
        else :
            return True
    
    def getCrossCenterDataForSHopfloor(self):
        arrangedata = ""
        for majorkey, subdict in ParameterList.SHIFTTHERSHOLD.iteritems():
            #print majorkey
            temp = self.getCrossCenterResultForShopfloor(majorkey)
            #items = temp[ParameterList.ITEMS]
            #value = str(temp[ParameterList.TESTVALUE])
            #result = temp[ParameterList.TESTRESULT]

            if temp[ParameterList.ITEMS] == None :
                items = ParameterList.NONE
            else :
                items = temp[ParameterList.ITEMS]
            
            if temp[ParameterList.TESTVALUE] == None :
                value = ParameterList.NONE
            else :
                value = str(temp[ParameterList.TESTVALUE])
            
            if temp[ParameterList.TESTRESULT] == None :
                result = ParameterList.FAIL
            else :
                result = temp[ParameterList.TESTRESULT]

            arrangedata += items + ":" + value + ":" + result + ";"
        
        return arrangedata

    
    def clearnMTFResultForShopfloor(self, firstkey, secendkey, value):
        if secendkey == "testresult" :
            self.__model__.mtfresultforshopfloor[firstkey][secendkey] = "FAIL"
        else :
            if secendkey == "testvalue" :
                self.__model__.mtfresultforshopfloor[firstkey][secendkey] = "None"
            else :
                self.__model__.mtfresultforshopfloor[firstkey][secendkey] = value

    def setMTFResultForShopfloor(self, firstkey, secendkey, value, fftthershold, currentfft, resultforui = None):
        if secendkey == "testresult" :
            if currentfft >= fftthershold :
                if self.__model__.mtfresultforshopfloor[firstkey]["testvalue"] >= float(value[firstkey]) :
                    self.__model__.mtfresultforshopfloor[firstkey][secendkey] = "PASS"
                    resultforui[firstkey] = "PASS"
                else :
                    self.__model__.mtfresultforshopfloor[firstkey][secendkey] = "FAIL"
                    resultforui[firstkey] = "FAIL"
            else :
                self.__model__.mtfresultforshopfloor[firstkey][secendkey] = "FAIL"
                resultforui[firstkey] = "FAIL"
        else :
            self.__model__.mtfresultforshopfloor[firstkey][secendkey] = value
        

    def getMTFResultForShopfloor(self, key):
        return self.__model__.mtfresultforshopfloor[key]
    
    def clearnMTFResult(self) :
        for majorkey, subdict in ParameterList.ROIs.iteritems():
            self.clearnMTFResultForShopfloor(majorkey, ParameterList.ITEMS , \
            majorkey)
            self.clearnMTFResultForShopfloor(majorkey, ParameterList.TESTVALUE , \
            majorkey)
            self.clearnMTFResultForShopfloor(majorkey, ParameterList.TESTRESULT , \
            majorkey)
    
    def getMTFDataForSHopfloor(self):
        arrangedata = ""
        for majorkey, subdict in ParameterList.ROIs.iteritems():
            temp = self.getMTFResultForShopfloor(majorkey)
            #print temp
            if temp[ParameterList.ITEMS] == None :
                items = ParameterList.NONE
            else :
                items = temp[ParameterList.ITEMS]
            
            if temp[ParameterList.TESTVALUE] == None :
                value = ParameterList.NONE
            else :
                value = str(temp[ParameterList.TESTVALUE])
            
            if temp[ParameterList.TESTRESULT] == None :
                result = ParameterList.FAIL
            else :
                result = temp[ParameterList.TESTRESULT]

            arrangedata += items + ":" + value + ":" + result + ";"
        
        return arrangedata