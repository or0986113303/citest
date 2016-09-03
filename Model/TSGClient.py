class Model(object):
    def __init__(self, station = None, employeeID = None, seriealnumber = None, customerseriealnumber = None, passorfail = None, resultdata = None):
        self.__station__ = station
        self.__employeeID__ = employeeID
        self.__seriealnumber__ = seriealnumber
        self.__customerseriealnumber__ = customerseriealnumber
        self.__passorfail__= passorfail
        self.__resultdata__ = resultdata
        self.ammetercheckresultforshopfloor = {"Power" : {"items" : None, "testvalue" : None, "testresult" : None}}
        self.colorcheckresultforshopfloor = {"RColor" : {"items" : None, "testvalue" : None, "testresult" : None}, \
        "GColor" : {"items" : None, "testvalue" : None, "testresult" : None}, \
        "BColor" : {"items" : None, "testvalue" : None, "testresult" : None}}
        self.fwcheckresultforshopfloor = {"FWVersion" : {"items" : None, "testvalue" : None, "testresult" : None}}
        self.crosscenterresultforshopfloor = {"XShift" : {"items" : None, "testvalue" : None, "testresult" : None}, \
        "YShift" : {"items" : None, "testvalue" : None, "testresult" : None}}
        self.mtfresultforshopfloor = {"LefttopField" : {"items" : None, "testvalue" : None, "testresult" : None} \
        , "LeftbuttonField" : {"items" : None, "testvalue" : None, "testresult" : None} \
        , "RighttopField" : {"items" : None, "testvalue" : None, "testresult" : None} \
        , "RightbuttonField" : {"items" : None, "testvalue" : None, "testresult" : None} \
        , "full" : {"items" : None, "testvalue" : None, "testresult" : None}}
        '''
        self.mtfresultforshopfloor = {"lefttop" : {"items" : None, "testvalue" : None, "testresult" : None} \
        , "leftbutton" : {"items" : None, "testvalue" : None, "testresult" : None} \
        , "righttop" : {"items" : None, "testvalue" : None, "testresult" : None} \
        , "rightbutton" : {"items" : None, "testvalue" : None, "testresult" : None} \
        , "center" : {"items" : None, "testvalue" : None, "testresult" : None} \
        , "full" : {"items" : None, "testvalue" : None, "testresult" : None}}
        '''

    def __del__(self):
        del self.__station__
        del self.__employeeID__
        del self.__seriealnumber__
        del self.__customerseriealnumber__
        del self.__passorfail__
        del self.__resultdata__
        del self.ammetercheckresultforshopfloor
        del self.colorcheckresultforshopfloor
        del self.fwcheckresultforshopfloor
        del self.crosscenterresultforshopfloor
        del self.mtfresultforshopfloor
    
    def getresultdata(self):
        return self.__resultdata__
    
    def setresultdata(self, value):
        self.__resultdata__ = value

    def getstation(self):
        return self.__station__
    
    def setstation(self, value):
        self.__station__ = value
    
    def getemployeeID(self):
        return self.__employeeID__
    
    def setemployeeID(self, value):
        self.__employeeID__ = value

    def getseriealnumber(self):
        return self.__seriealnumber__
    
    def setseriealnumber(self, value):
        self.__seriealnumber__ = value

    def getcustomerseriealnumber(self):
        return self.__customerseriealnumber__
    
    def setcustomerseriealnumber(self, value):
        self.__customerseriealnumber__ = value
    
    def getpassorfail(self):
        return self.__passorfail__
    
    def setpassorfail(self, value):
        self.__passorfail__ = value

        
