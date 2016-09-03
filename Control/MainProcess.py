# -*- coding: utf-8 -*-

#import cv2
#import cv2.cv as cv
import numpy as np
import time
from threading import *

from Model import ParameterList
from Control import Arduino
from Control import MTF
from Control import Camera
from Control import TSGClient
from Control import CrossCenter
from Control import ColorSpace
from Control import Ammeter


class MainProcess(Thread):
    def __init__(self, condition, dataevent, request, drawevent, sleeptime=0.03):
    #Run the MainLoop as a thread. Access the frame with self.frame.
        """
        Initialize image process variable
        """
        Thread.__init__(self)
        # declare thread control variable
        self.con = condition
        self.con.acquire()

        # declare binaryfile to write
        self.__FWFile__ = None
        
        # declare request member
        self.__request__ = request

        # declare data event member
        self.__dataevent__ = dataevent

        # declare draw Event
        self.__drawevent__ = drawevent

        # declare main loop delay time default 0.03 sec
        self.__sleeptime__ = sleeptime

        # declare MTF parts data
        self.__ESF__ = {ParameterList.CENTER:{}, ParameterList.LEFTTOP:{}, \
        ParameterList.LEFTBUTTON:{}, ParameterList.RIGHTTOP:{}, ParameterList.RIGHTBUTTON:{}}
        self.__LSF__ = {ParameterList.CENTER:{}, ParameterList.LEFTTOP:{}, \
        ParameterList.LEFTBUTTON:{}, ParameterList.RIGHTTOP:{}, ParameterList.RIGHTBUTTON:{}}
        self.__MTF__ = {ParameterList.CENTER:{}, ParameterList.LEFTTOP:{}, \
        ParameterList.LEFTBUTTON:{}, ParameterList.RIGHTTOP:{}, ParameterList.RIGHTBUTTON:{}}
        self.__MTFData__ = {ParameterList.CENTER:{}, ParameterList.LEFTTOP:{}, \
        ParameterList.LEFTBUTTON:{}, ParameterList.RIGHTTOP:{}, ParameterList.RIGHTBUTTON:{}}
        self.__IXData__ = {ParameterList.CENTER:{}, ParameterList.LEFTTOP:{}, \
        ParameterList.LEFTBUTTON:{}, ParameterList.RIGHTTOP:{}, ParameterList.RIGHTBUTTON:{}}
        self.__POLYData__ = {ParameterList.CENTER:{}, ParameterList.LEFTTOP:{}, \
        ParameterList.LEFTBUTTON:{}, ParameterList.RIGHTTOP:{}, ParameterList.RIGHTBUTTON:{}}

        # declare ROI data
        self.__SRCROI__ = {ParameterList.CENTER:{}, ParameterList.LEFTTOP:{}, \
        ParameterList.LEFTBUTTON:{}, ParameterList.RIGHTTOP:{}, ParameterList.RIGHTBUTTON:{}, \
        ParameterList.PATTERN:{}}

        # declare MTF kernel
        self.__MTFKernel__ = MTF.Control()
        self.__MTFKernel__.setMTFModel(ParameterList.IMG_WIDTH, ParameterList.IMG_HEIGHT)
        
        # delcare webcamre and initialize it
        self.__Camera__ = Camera.Control(ParameterList.IMG_WIDTH, ParameterList.IMG_HEIGHT, ParameterList.CAMERAID)

        # camera connect
        self.__Camera__.connect()

        # declare arduino plateform controller
        self.__ArduinoControl__ = Arduino.Control()

        # declare shopfloor communication
        self.__Shopfloor__ = TSGClient.Control()

        # declare cross center detector
        self.__CrossCenter__ = CrossCenter.Control(ParameterList.PATTERNSIZE, (ParameterList.IMG_WIDTH, ParameterList.IMG_HEIGHT))

        # declare color space dectect
        self.__colorspace__ = ColorSpace.Control()

        # declare xyshift value
        self.__shiftXYresult__ = None

        # declare fw check total result
        self.__FWTotalResult__ = False

        # declare mtf total result
        self.__MTFTotalResult__ = False

        # declare cross center total result
        self.__CrossCenterTotalResult__ = False

        # declare color check total result
        self.__ColorTotalResult__ = False

        # declare ammeter check total result
        self.__AmmeterTotalResult__ = False

        # declare ammeter controller
        self.__Ammeter__ = Ammeter.Control()
        
        self.__Shopfloor__.setcustomerseriealnumber(ParameterList.WORKINGSTATION[ParameterList.CUSTOMERSERIALNUMBER])
        self.__Shopfloor__.setemployeeID( ParameterList.WORKINGSTATION[ParameterList.EMPLOYEEID])
        self.__Shopfloor__.setstation(ParameterList.WORKINGSTATION[ParameterList.STATIONNAME])
        
        self.__Shopfloor__.setpassorfail(ParameterList.FAIL)

        ##self.__Shopfloor__.Connect()

        # waitting for shopfloor connect the server
        ##time.sleep(float(ParameterList.CONFIGURE[ParameterList.WAKEUPTIME]))

        ##self.__Shopfloor__.CheckStationAndEmployeeID()
        #self.__Shopfloor__.CheckStationAndSeriealNumber()

    def __del__(self):
        del self.__Camera__
        del self.__ArduinoControl__
        del self.__SRCROI__
        del self.__ESF__
        del self.__LSF__
        del self.__MTF__
        del self.__MTFData__
        del self.__IXData__
        del self.__POLYData__
        ##del self.__Shopfloor__
        del self.__FWFile__        
        del self.con
        del self.__sleeptime__
        del self.__request__
        del self.__dataevent__ 
        del self.__drawevent__
        del self.__Ammeter__
        

    def release(self):
        ##self.__Shopfloor__.DisConnect()
        self.__del__()

    def __getMTFResult__(self) :
        statuscounter = 0
        for majorkey, subdict in ParameterList.ROIs.iteritems():
            #print majorkey
            self.__ESF__[majorkey] = self.__MTFKernel__.getESF(self.__SRCROI__[majorkey])
            self.__LSF__[majorkey] = self.__MTFKernel__.getLSF(self.__ESF__[majorkey])
            self.__MTF__[majorkey] = self.__MTFKernel__.getMTF(self.__LSF__[majorkey])

        for majorkey, subdict in ParameterList.ROIs.iteritems():
            self.__MTFData__[majorkey] = self.__MTF__[majorkey][0]
            self.__IXData__[majorkey] = self.__MTF__[majorkey][1]
            self.__POLYData__[majorkey] = self.__MTF__[majorkey][2]
            self.__Camera__.setMTF50Result(majorkey, \
            self.__POLYData__[majorkey](self.__IXData__[majorkey]) \
            [len(self.__POLYData__[majorkey](self.__IXData__[majorkey])) / 2])

            self.__Shopfloor__.setMTFResultForShopfloor(majorkey, ParameterList.ITEMS , \
            majorkey, ParameterList.FFTTHERSHOLD, self.__MTFKernel__.getGlobalFFTValue())

            self.__Shopfloor__.setMTFResultForShopfloor(majorkey, ParameterList.TESTVALUE , \
            self.__Camera__.getMTF50Result(majorkey), ParameterList.FFTTHERSHOLD, self.__MTFKernel__.getGlobalFFTValue())

            self.__Shopfloor__.setMTFResultForShopfloor(majorkey, ParameterList.TESTRESULT , \
            ParameterList.MTFTHERSHOLD, ParameterList.FFTTHERSHOLD, self.__MTFKernel__.getGlobalFFTValue(), ParameterList.MTFRESULT)

            if ParameterList.MTFRESULT[majorkey] == ParameterList.FAIL : 
                statuscounter += 1
        
        if statuscounter > 0:
            return False
        else :
            return True

    def __getMTFROIs__(self, img) :
        for majorkey, subdict in ParameterList.ROIs.iteritems():
            tmp = img[int(subdict[1]) : int(subdict[1] + ParameterList.ROIH),\
            int(subdict[0]) :int(subdict[0] + ParameterList.ROIW) ]
            self.__SRCROI__[majorkey] = 0.299*tmp[:,:,0] + 0.589*tmp[:,:,1]+0.114*tmp[:,:,2]
    
    def __getPatternROI__(self, img):
        
        self.__SRCROI__[ParameterList.PATTERN] = img[\
        int(ParameterList.PATTERNROI[ParameterList.PATTERN][1]) : int(ParameterList.PATTERNROI[ParameterList.PATTERN][1] + ParameterList.PATTERNH),\
        int(ParameterList.PATTERNROI[ParameterList.PATTERN][0]) : int(ParameterList.PATTERNROI[ParameterList.PATTERN][0] + ParameterList.PATTERNW)]
    
    def __getBinaryfile__(self):
        self.__FWFile__ = open(ParameterList.BINARYFILEPATH, "rb").read()
        
    def run(self):
        """
        Main thread function
        """
        self.__getBinaryfile__()
        self.__request__["startRequest"].wait()
        while self.__request__["startRequest"].isSet():
            time.sleep(self.__sleeptime__)
            
            if self.__request__["seriealRequest"].isSet():
                if ParameterList.LINEINFORMATION[ParameterList.TYPE] == ParameterList.SA :
                    self.__AmmeterTotalResult__ = False
                    self.__ColorTotalResult__ = False
                    self.__FWTotalResult__ = False
                    self.__MTFTotalResult__ = False
                    self.__CrossCenterTotalResult__ = False
                    self.__Shopfloor__.clearnMTFResult()
                    self.__Shopfloor__.clearnCrossCenterResult()
                    self.__Shopfloor__.clearnFWVersionCheckResult()
                    self.__Shopfloor__.clearnColorCheckResult()
                    self.__Shopfloor__.clreanAmmeterResult()
                elif ParameterList.LINEINFORMATION[ParameterList.TYPE] == ParameterList.FA :
                    self.__ColorTotalResult__ = False
                    self.__MTFTotalResult__ = False
                    self.__CrossCenterTotalResult__ = False
                    self.__Shopfloor__.clearnMTFResult()
                    self.__Shopfloor__.clearnCrossCenterResult()
                    self.__Shopfloor__.clearnColorCheckResult()

                self.__Camera__.grabFrame()
                RGBImage = self.__Camera__.getCurrentRGBImage()
                GrayImage = self.__Camera__.getCurrentGrayImage()
                SmoothGrayImage = self.__Camera__.getSmoothGrayImage()
                self.__Shopfloor__.setseriealnumber(ParameterList.WORKINGSTATION[ParameterList.SERIALNUMBER])
                data = self.__Shopfloor__.CheckStationAndSeriealNumber()
                #print data
                if data["result"] :
                    self.__dataevent__["seriealcheck"].SetData(ParameterList.PASS, self.__Camera__.getStatusImage(ParameterList.SERIAL + ParameterList.PASS))
                else :
                    self.__dataevent__["seriealcheck"].SetData(ParameterList.FAIL, self.__Camera__.getStatusImage(data["message"] + data["errorcode"]))
                self.__drawevent__["drawStatus"].wait()
                self.__drawevent__["drawStatus"].clear()

            if self.__request__["ammeterRequest"].isSet():
                #if ParameterList.LINEINFORMATION[ParameterList.TYPE] == ParameterList.SA :
                #    self.__Shopfloor__.clearnMTFResult()
                #    self.__Shopfloor__.clearnCrossCenterResult()
                #    self.__Shopfloor__.clearnFWVersionCheckResult()
                #    self.__Shopfloor__.clearnColorCheckResult()
                #    self.__Shopfloor__.clreanAmmeterResult()

                self.__Camera__.grabFrame()
                RGBImage = self.__Camera__.getCurrentRGBImage()
                GrayImage = self.__Camera__.getCurrentGrayImage()
                SmoothGrayImage = self.__Camera__.getSmoothGrayImage()

                value = 0
                counter = 0
                graduation = ""
                unit = ""

                if self.__Ammeter__.connect(comport = ParameterList.CONFIGURE[ParameterList.AMMETERPORT], baudrate = int(ParameterList.CONFIGURE[ParameterList.AMMETERBAUDRATE]), \
                type = ParameterList.WORKINGSTATION[ParameterList.AMMETERSELECT]) :
                    self.__dataevent__["ammetercheck"].SetData(ParameterList.ING, self.__Camera__.getStatusImage(ParameterList.AMMETERCHECK + ParameterList.ING + ParameterList.DOT))
                    self.__drawevent__["drawStatus"].wait()
                    self.__drawevent__["drawStatus"].clear()
                    for i in range(0,5,1):
                        value += self.__Ammeter__.readvalue()
                        counter += 1
                        time.sleep(float(ParameterList.CONFIGURE[ParameterList.DISPLAYTIME]))
                    value /= counter
                    graduation = self.__Ammeter__.getgraduation()
                    unit = self.__Ammeter__.getunit()
                    self.__Ammeter__.disconnect()
                    self.__AmmeterTotalResult__ = True
                else :
                    self.__Ammeter__.disconnect()
                    self.__AmmeterTotalResult__ = False

                self.__Ammeter__.setThershold(ParameterList.AMMETERTHERSHOLD)

                if unit == self.__Ammeter__.getThershold("unit") :
                    if graduation == self.__Ammeter__.getThershold("graduation") :
                        if value <= float(self.__Ammeter__.getThershold(ParameterList.UPPERVALUE)) and value >= float(self.__Ammeter__.getThershold(ParameterList.LOWERVALUE)):
                            self.__Shopfloor__.getAmmeterResult({"items" : graduation + unit, "testvalue" : value, "testresult" : ParameterList.PASS})
                            self.__AmmeterTotalResult__ = True
                        else :
                            self.__Shopfloor__.getAmmeterResult({"items" : graduation + unit, "testvalue" : value, "testresult" : ParameterList.FAIL})
                            self.__AmmeterTotalResult__ = False
                    else :
                        self.__Shopfloor__.getAmmeterResult({"items" : graduation + unit, "testvalue" : value, "testresult" : ParameterList.FAIL})
                        self.__AmmeterTotalResult__ = False
                else :
                    self.__Shopfloor__.getAmmeterResult({"items" : graduation + unit, "testvalue" : value, "testresult" : ParameterList.FAIL})
                    self.__AmmeterTotalResult__ = False
                if self.__AmmeterTotalResult__ :
                    self.__dataevent__["ammetercheck"].SetData(ParameterList.PASS, self.__Camera__.getStatusImage(str(value) + graduation + unit + " " + ParameterList.PASS))
                else :
                    self.__dataevent__["ammetercheck"].SetData(ParameterList.FAIL, self.__Camera__.getStatusImage(str(value) + graduation + unit + " " + ParameterList.FAIL))
                self.__drawevent__["drawStatus"].wait()
                self.__drawevent__["drawStatus"].clear()

                
            if self.__request__["fwcheckRequest"].isSet():
                
                self.__Camera__.grabFrame()
                RGBImage = self.__Camera__.getCurrentRGBImage()
                GrayImage = self.__Camera__.getCurrentGrayImage()
                SmoothGrayImage = self.__Camera__.getSmoothGrayImage()

                if self.__ArduinoControl__.connect(ParameterList.CONFIGURE[ParameterList.FIXTUREPORT], int(ParameterList.CONFIGURE[ParameterList.FIXTUREBAUDRATE])) :
                    time.sleep(float(ParameterList.CONFIGURE[ParameterList.WAKEUPTIME]))
                    
                    if self.__ArduinoControl__.checkfwversion() :
                        self.__ArduinoControl__.disconnect()
                        self.__FWTotalResult__ = True
                        self.__Shopfloor__.getFWVersionCheckResult(self.__FWTotalResult__)
                        self.__dataevent__["fwcheck"].SetData(ParameterList.PASS, self.__Camera__.getStatusImage(ParameterList.FWCHECK + ParameterList.PASS))
                        self.__drawevent__["drawStatus"].wait()
                        self.__drawevent__["drawStatus"].clear()
                    else :
                        self.__ArduinoControl__.disconnect()
                        self.__FWTotalResult__ = False
                        self.__Shopfloor__.getFWVersionCheckResult(self.__FWTotalResult__)
                        self.__dataevent__["fwcheck"].SetData(ParameterList.FAIL, self.__Camera__.getStatusImage(ParameterList.FWCHECK + ParameterList.FAIL))
                        self.__drawevent__["drawStatus"].wait()
                        self.__drawevent__["drawStatus"].clear()
                else :
                    self.__ArduinoControl__.disconnect()
                    self.__FWTotalResult__ = False
                    self.__Shopfloor__.getFWVersionCheckResult(self.__FWTotalResult__)
                    self.__dataevent__["fwcheck"].SetData(ParameterList.FAIL, self.__Camera__.getStatusImage(ParameterList.COMPORT +\
                    ParameterList.FAIL))
                    self.__drawevent__["drawStatus"].wait()
                    self.__drawevent__["drawStatus"].clear()
                time.sleep(float(ParameterList.CONFIGURE[ParameterList.DISPLAYTIME]))
            
            if self.__request__["colorcheckRequest"].isSet():
                checkcounter = 0
                self.__colorspace__.setCondition(ParameterList.COLORCONDITION)
                successtemp = {ParameterList.RCHANNEL : 0, ParameterList.GCHANNEL : 0, ParameterList.BCHANNEL : 0, "Result" : False}
                failstemp = {ParameterList.RCHANNEL : 0, ParameterList.GCHANNEL : 0, ParameterList.BCHANNEL : 0, "Result" : False}
                #result = {ParameterList.RCHANNEL : 0, ParameterList.GCHANNEL : 0, ParameterList.BCHANNEL : 0, "Result" : None}
                for i in range(0,5,1):
                    self.__Camera__.grabFrame()
                    time.sleep(0.1)
                for i in range(0,30,1):
                    self.__Camera__.grabFrame()
                    RGBImage = self.__Camera__.getCurrentRGBImage()
                    GrayImage = self.__Camera__.getCurrentGrayImage()
                    SmoothGrayImage = self.__Camera__.getSmoothGrayImage()
                    self.__colorspace__.setSourceImage(RGBImage)
                    result = self.__colorspace__.caculatecolor()
                    #print result[ParameterList.RCHANNEL]
                    #print result[ParameterList.GCHANNEL]
                    #print result[ParameterList.BCHANNEL]
                    
                    self.__dataevent__["colorcheck"].SetData(ParameterList.ING, self.__Camera__.getStatusImage(ParameterList.COLORCHECK + ParameterList.PASS), RGBImage)
                    self.__drawevent__["drawStatus"].wait()
                    self.__drawevent__["drawStatus"].clear()
                    #print result
                    if result["Result"] : 
                        successtemp[ParameterList.RCHANNEL] += int(result[ParameterList.RCHANNEL])
                        successtemp[ParameterList.GCHANNEL] += int(result[ParameterList.GCHANNEL])
                        successtemp[ParameterList.BCHANNEL] += int(result[ParameterList.BCHANNEL])
                        checkcounter += 1
                    else : 
                        failstemp[ParameterList.RCHANNEL] += int(result[ParameterList.RCHANNEL])
                        failstemp[ParameterList.GCHANNEL] += int(result[ParameterList.GCHANNEL])
                        failstemp[ParameterList.BCHANNEL] += int(result[ParameterList.BCHANNEL])
                #print checkcounter
                #temp[ParameterList.RCHANNEL] /= 30
                #temp[ParameterList.GCHANNEL] /= 30
                #temp[ParameterList.BCHANNEL] /= 30

                if checkcounter >= 25 : 
                    successtemp[ParameterList.RCHANNEL] /= checkcounter
                    successtemp[ParameterList.GCHANNEL] /= checkcounter
                    successtemp[ParameterList.BCHANNEL] /= checkcounter 
                    successtemp["Result"] = True
                    #print temp
                    self.__ColorTotalResult__ = True
                    self.__Shopfloor__.getColorCheckResult(successtemp)
                    self.__dataevent__["colorcheck"].SetData(ParameterList.PASS, self.__Camera__.getStatusImage(ParameterList.COLORCHECK + ParameterList.PASS), RGBImage)
                    self.__drawevent__["drawStatus"].wait()
                    self.__drawevent__["drawStatus"].clear()
                else :
                    failstemp[ParameterList.RCHANNEL] /= (30 - checkcounter)
                    failstemp[ParameterList.GCHANNEL] /= (30 - checkcounter)
                    failstemp[ParameterList.BCHANNEL] /= (30 - checkcounter) 
                    failstemp["Result"] = False
                    #print temp
                    self.__Shopfloor__.getColorCheckResult(failstemp)
                    self.__ColorTotalResult__ = False
                    self.__dataevent__["colorcheck"].SetData(ParameterList.FAIL, self.__Camera__.getStatusImage(ParameterList.COLORCHECK + ParameterList.FAIL), RGBImage)
                    self.__drawevent__["drawStatus"].wait()
                    self.__drawevent__["drawStatus"].clear()
                time.sleep(float(ParameterList.CONFIGURE[ParameterList.DISPLAYTIME]))

            if self.__request__["caculateRequest"].isSet():
                
                #if ParameterList.LINEINFORMATION[ParameterList.TYPE] == ParameterList.FA :
                #    self.__Shopfloor__.clearnMTFResult()
                #    self.__Shopfloor__.clearnCrossCenterResult()
                #    self.__Shopfloor__.clearnColorCheckResult()

                self.__MTFTotalResult__ = False

                self.__Camera__.grabFrame()
                RGBImage = self.__Camera__.getCurrentRGBImage()
                GrayImage = self.__Camera__.getCurrentGrayImage()
                SmoothGrayImage = self.__Camera__.getSmoothGrayImage()
                frame_dft = self.__MTFKernel__.get2DDFT(SmoothGrayImage)

                self.__getMTFROIs__(RGBImage)

                self.__MTFTotalResult__ = self.__getMTFResult__()
                self.__MTFKernel__.drawROIs(RGBImage, ParameterList.ROICOLOR, ParameterList.ROIs, ParameterList.ROIW, ParameterList.ROIH)
                self.__MTFKernel__.drawResult(RGBImage, ParameterList.ROICOLOR, ParameterList.ROIs, ParameterList.MTFRESULT)
                self.__dataevent__["ImageIn"].SetData(RGBImage, self.__Camera__.getStatusImage(ParameterList.FOCUS + \
                ParameterList.ING + ParameterList.DOT), self.__MTFTotalResult__)
                self.__drawevent__["drawcameraview"].wait()
                self.__drawevent__["drawcameraview"].clear()
                self.__dataevent__["DFTIn"].SetData(frame_dft)
                self.__drawevent__["drawDFT"].wait()
                self.__drawevent__["drawDFT"].clear()
                self.__dataevent__["MTFIn"].SetData(self.__MTFData__, self.__IXData__, self.__POLYData__, self.__MTFTotalResult__)
                self.__drawevent__["drawMTF"].wait()
                self.__drawevent__["drawMTF"].clear()
                

            if self.__request__["flushRequest"].isSet():
                if self.__ArduinoControl__.connect(ParameterList.CONFIGURE[ParameterList.FIXTUREPORT], int(ParameterList.CONFIGURE[ParameterList.FIXTUREBAUDRATE])) :
                    self.__dataevent__["Flush"].SetData(ParameterList.ING, self.__Camera__.getStatusImage(ParameterList.FLUSH + \
                    ParameterList.ING + ParameterList.DOT))
                    self.__drawevent__["drawStatus"].wait()
                    self.__drawevent__["drawStatus"].clear()
                    time.sleep(float(ParameterList.CONFIGURE[ParameterList.WAKEUPTIME]))
                    self.__ArduinoControl__.setbinaryfile(self.__FWFile__)
                    self.__ArduinoControl__.reduceXYshift(self.__shiftXYresult__, ParameterList.SHIFTTHERSHOLD, ParameterList.SENSORPIXELSCALE)
                    self.__ArduinoControl__.recaculatechecksum()

                    if self.__ArduinoControl__.checkcurrectstart() :
                        if self.__ArduinoControl__.sendbinaryfile() :
                            if self.__ArduinoControl__.checkwriteeeprom() :
                                self.__ArduinoControl__.disconnect()
                                self.__dataevent__["Flush"].SetData(ParameterList.PASS, self.__Camera__.getStatusImage(ParameterList.FLUSH + ParameterList.DONE))
                                self.__drawevent__["drawStatus"].wait()
                                self.__drawevent__["drawStatus"].clear()
                            else : 
                                self.__ArduinoControl__.disconnect()
                                self.__dataevent__["Flush"].SetData(ParameterList.FAIL, self.__Camera__.getStatusImage(ParameterList.I2C + ParameterList.FAIL))
                                self.__drawevent__["drawStatus"].wait()
                                self.__drawevent__["drawStatus"].clear()
                        else :
                            self.__ArduinoControl__.disconnect()
                            self.__dataevent__["Flush"].SetData(ParameterList.FAIL, self.__Camera__.getStatusImage(ParameterList.COMPORT +\
                            ParameterList.FAIL))
                            self.__drawevent__["drawStatus"].wait()
                            self.__drawevent__["drawStatus"].clear()
                    else :
                        self.__ArduinoControl__.disconnect()
                        self.__dataevent__["Flush"].SetData(ParameterList.FAIL, self.__Camera__.getStatusImage(ParameterList.I2C + ParameterList.FAIL))
                        self.__drawevent__["drawStatus"].wait()
                        self.__drawevent__["drawStatus"].clear()
                else :
                    self.__dataevent__["Flush"].SetData(ParameterList.FAIL, self.__Camera__.getStatusImage(ParameterList.COMPORT +\
                            ParameterList.FAIL))
                    self.__drawevent__["drawStatus"].wait()
                    self.__drawevent__["drawStatus"].clear()
            
            if self.__request__["recordRequest"].isSet():
                time.sleep(float(ParameterList.CONFIGURE[ParameterList.WAKEUPTIME]))
                self.__dataevent__["Record"].SetData(ParameterList.ING, self.__Camera__.getStatusImage(ParameterList.RECORD + \
                ParameterList.ING +ParameterList.DOT))
                self.__drawevent__["drawStatus"].wait()
                self.__drawevent__["drawStatus"].clear()
                time.sleep(float(ParameterList.CONFIGURE[ParameterList.DISPLAYTIME]))

                if ParameterList.LINEINFORMATION[ParameterList.TYPE] == ParameterList.SA :
                    if not self.__AmmeterTotalResult__ :
                        resultstring = ParameterList.AMMETERCHECK + ParameterList.FAIL
                    elif not self.__FWTotalResult__ :
                        resultstring = ParameterList.FWCHECK + ParameterList.FAIL
                    elif not self.__ColorTotalResult__ :
                        resultstring = ParameterList.COLORCHECK + ParameterList.FAIL
                    elif not self.__MTFTotalResult__ :
                        resultstring = ParameterList.MTF + ParameterList.FAIL
                    elif not self.__CrossCenterTotalResult__ :
                        resultstring = ParameterList.CROSSCENTER + ParameterList.FAIL
                    else :
                        resultstring = ParameterList.PASS
                    
                    if resultstring == ParameterList.PASS :
                        self.__Shopfloor__.setpassorfail(ParameterList.PASS)
                    else :
                        self.__Shopfloor__.setpassorfail(ParameterList.FAIL)
                        
                    data = self.__Shopfloor__.getAmmeterResultForShopfloor() + \
                    self.__Shopfloor__.getFWVersionCheckResultForSHopfloor() + \
                    self.__Shopfloor__.getColorCheckDataForSHopfloor() + \
                    self.__Shopfloor__.getMTFDataForSHopfloor() + \
                    self.__Shopfloor__.getCrossCenterDataForSHopfloor()
                    self.__Shopfloor__.setresultdata(data)
                    self.__Shopfloor__.CheckTestResult()
                    self.__Shopfloor__.CheckPassOrFail()
                    '''
                    if self.__AmmeterTotalResult__ :
                        self.__Shopfloor__.setpassorfail(ParameterList.PASS)
                    else :
                        self.__Shopfloor__.setpassorfail(ParameterList.FAIL)
                    self.__Shopfloor__.setresultdata(self.__Shopfloor__.getAmmeterResultForShopfloor())
                    self.__Shopfloor__.CheckTestResult()
                    self.__Shopfloor__.CheckPassOrFail()

                    if self.__FWTotalResult__ :
                        self.__Shopfloor__.setpassorfail(ParameterList.PASS)
                    else : 
                        self.__Shopfloor__.setpassorfail(ParameterList.FAIL)
                    self.__Shopfloor__.setresultdata(self.__Shopfloor__.getFWVersionCheckResultForSHopfloor())
                    self.__Shopfloor__.CheckTestResult()
                    self.__Shopfloor__.CheckPassOrFail()

                    if self.__ColorTotalResult__ :
                        self.__Shopfloor__.setpassorfail(ParameterList.PASS)
                    else : 
                        self.__Shopfloor__.setpassorfail(ParameterList.FAIL)
                    #print self.__Shopfloor__.getColorCheckDataForSHopfloor()
                    self.__Shopfloor__.setresultdata(self.__Shopfloor__.getColorCheckDataForSHopfloor())
                    self.__Shopfloor__.CheckTestResult()
                    self.__Shopfloor__.CheckPassOrFail()

                    if self.__MTFTotalResult__ :
                        self.__Shopfloor__.setpassorfail(ParameterList.PASS)
                    else : 
                        self.__Shopfloor__.setpassorfail(ParameterList.FAIL)
                    self.__Shopfloor__.setresultdata(self.__Shopfloor__.getMTFDataForSHopfloor())
                    self.__Shopfloor__.CheckTestResult()
                    self.__Shopfloor__.CheckPassOrFail()

                    if self.__CrossCenterTotalResult__ :
                        self.__Shopfloor__.setpassorfail(ParameterList.PASS)
                    else : 
                        self.__Shopfloor__.setpassorfail(ParameterList.FAIL)
                    self.__Shopfloor__.setresultdata(self.__Shopfloor__.getCrossCenterDataForSHopfloor())
                    self.__Shopfloor__.CheckTestResult()
                    self.__Shopfloor__.CheckPassOrFail()
                    '''
                elif ParameterList.LINEINFORMATION[ParameterList.TYPE] == ParameterList.FA :
                    if not self.__ColorTotalResult__ :
                        resultstring = ParameterList.COLORCHECK + ParameterList.FAIL
                    elif not self.__MTFTotalResult__ :
                        resultstring = ParameterList.MTF + ParameterList.FAIL
                    elif not self.__CrossCenterTotalResult__ :
                        resultstring = ParameterList.CROSSCENTER + ParameterList.FAIL
                    else :
                        resultstring = ParameterList.PASS
                    
                    if resultstring == ParameterList.PASS :
                        self.__Shopfloor__.setpassorfail(ParameterList.PASS)
                    else :
                        self.__Shopfloor__.setpassorfail(ParameterList.FAIL)

                    data = self.__Shopfloor__.getColorCheckDataForSHopfloor() + self.__Shopfloor__.getMTFDataForSHopfloor() + self.__Shopfloor__.getCrossCenterDataForSHopfloor()
                    self.__Shopfloor__.setresultdata(data)
                    self.__Shopfloor__.CheckTestResult()
                    self.__Shopfloor__.CheckPassOrFail()

                    '''
                    if self.__ColorTotalResult__ :
                        self.__Shopfloor__.setpassorfail(ParameterList.PASS)
                    else : 
                        self.__Shopfloor__.setpassorfail(ParameterList.FAIL)
                    self.__Shopfloor__.setresultdata(self.__Shopfloor__.getColorCheckDataForSHopfloor())
                    self.__Shopfloor__.CheckTestResult()
                    self.__Shopfloor__.CheckPassOrFail()
                    
                    if self.__MTFTotalResult__ :
                        self.__Shopfloor__.setpassorfail(ParameterList.PASS)
                    else : 
                        self.__Shopfloor__.setpassorfail(ParameterList.FAIL)
                    self.__Shopfloor__.setresultdata(self.__Shopfloor__.getMTFDataForSHopfloor())
                    self.__Shopfloor__.CheckTestResult()
                    self.__Shopfloor__.CheckPassOrFail()

                    if self.__CrossCenterTotalResult__ :
                        self.__Shopfloor__.setpassorfail(ParameterList.PASS)
                    else : 
                        self.__Shopfloor__.setpassorfail(ParameterList.FAIL)
                    self.__Shopfloor__.setresultdata(self.__Shopfloor__.getCrossCenterDataForSHopfloor())
                    self.__Shopfloor__.CheckTestResult()
                    self.__Shopfloor__.CheckPassOrFail()
                    '''
                self.__dataevent__["Record"].SetData(ParameterList.PASS, self.__Camera__.getStatusImage(ParameterList.RECORD + ParameterList.DONE))
                self.__drawevent__["drawStatus"].wait()
                self.__drawevent__["drawStatus"].clear()
            
            if self.__request__["crosscenterRequest"].isSet():
                self.__CrossCenterTotalResult__ = False
                for i in range(0,30,1):
                    shiftXY = None
                    self.__Camera__.grabFrame()
                    RGBImage = self.__Camera__.getCurrentRGBImage()
                    GrayImage = self.__Camera__.getCurrentGrayImage()
                    self.__getPatternROI__(GrayImage)

                    self.__CrossCenter__.drawSensorCenter(RGBImage, ParameterList.IMG_WIDTH, ParameterList.IMG_HEIGHT)
                    
                    #self.__CrossCenter__.setColorShadeROIs(GrayImage, ParameterList.COLORSHADEREFPOINT, ParameterList.COLORSHADEROISIZE)

                    #shiftXY = self.__CrossCenter__.caculateColorShadeArea(ParameterList.COLORSHADEREFPOINT, ParameterList.COLORSHADEROISIZE)
                    
                    #self.__CrossCenter__.drawColorShadeROI(RGBImage, ParameterList.COLORSHADEREFPOINT, ParameterList.COLORSHADEROISIZE)
                    #self.__CrossCenter__.setCenterShiftSequere(shiftXY,i)

                    self.__CrossCenter__.patterndetect(self.__SRCROI__[ParameterList.PATTERN])
                    self.__CrossCenter__.caculatecenter(ParameterList.PATTERNOFFSET)
                
                #self.__shiftXYresult__ = None
                #self.__shiftXYresult__ = self.__CrossCenter__.getCenterShiftValue()
                #self.__CrossCenterTotalResult__ = self.__Shopfloor__.getCrossCenterResult(self.__shiftXYresult__)
                #self.__CrossCenter__.drawColorShadeResult(RGBImage,self.__shiftXYresult__)
                self.__shiftXYresult__ = None
                self.__shiftXYresult__ = self.__CrossCenter__.getHolderLensShiftValue(ParameterList.IMG_WIDTH, ParameterList.IMG_HEIGHT, ParameterList.CONFIGURE)
                #print self.__shiftXYresult__
                self.__CrossCenter__.drawColorShadeResult(RGBImage, self.__shiftXYresult__)
                #self.__CrossCenter__.drawResult(RGBImage,ParameterList.PATTERNOFFSET)
                self.__CrossCenterTotalResult__ = self.__Shopfloor__.getCrossCenterResult(self.__shiftXYresult__)
                #self.__CrossCenterTotalResult__ = False
                if self.__CrossCenterTotalResult__ : 
                    self.__dataevent__["CrossCenter"].SetData(RGBImage, self.__Camera__.getStatusImage(ParameterList.CROSSCENTER + \
                    ParameterList.PASS), self.__CrossCenterTotalResult__)
                else :
                    self.__dataevent__["CrossCenter"].SetData(RGBImage, self.__Camera__.getStatusImage(ParameterList.CROSSCENTER + \
                    ParameterList.FAIL), self.__CrossCenterTotalResult__)
                
                self.__drawevent__["drawCrossCenter"].wait()
                self.__drawevent__["drawCrossCenter"].clear()
            
            if self.__request__["statusdisplayRequest"].isSet() :
                resultstring = ""
                if ParameterList.LINEINFORMATION[ParameterList.TYPE] == ParameterList.SA :
                    if not self.__AmmeterTotalResult__ :
                        resultstring = ParameterList.AMMETERCHECK + ParameterList.FAIL
                    elif not self.__FWTotalResult__ :
                        resultstring = ParameterList.FWCHECK + ParameterList.FAIL
                    elif not self.__ColorTotalResult__ :
                        resultstring = ParameterList.COLORCHECK + ParameterList.FAIL
                    elif not self.__MTFTotalResult__ :
                        resultstring = ParameterList.MTF + ParameterList.FAIL
                    elif not self.__CrossCenterTotalResult__ :
                        resultstring = ParameterList.CROSSCENTER + ParameterList.FAIL
                    else :
                        resultstring = ParameterList.PASS
                    self.__AmmeterTotalResult__ = False
                    self.__ColorTotalResult__ = False
                    self.__FWTotalResult__ = False
                    self.__MTFTotalResult__ = False
                    self.__CrossCenterTotalResult__ = False
                    self.__Shopfloor__.clearnMTFResult()
                    self.__Shopfloor__.clearnCrossCenterResult()
                    self.__Shopfloor__.clearnFWVersionCheckResult()
                    self.__Shopfloor__.clearnColorCheckResult()
                    self.__Shopfloor__.clreanAmmeterResult()
                elif ParameterList.LINEINFORMATION[ParameterList.TYPE] == ParameterList.FA :
                    if not self.__ColorTotalResult__ :
                        resultstring = ParameterList.COLORCHECK + ParameterList.FAIL
                    elif not self.__MTFTotalResult__ :
                        resultstring = ParameterList.MTF + ParameterList.FAIL
                    elif not self.__CrossCenterTotalResult__ :
                        resultstring = ParameterList.CROSSCENTER + ParameterList.FAIL
                    else :
                        resultstring = ParameterList.PASS
                    self.__ColorTotalResult__ = False
                    self.__MTFTotalResult__ = False
                    self.__CrossCenterTotalResult__ = False
                    self.__Shopfloor__.clearnMTFResult()
                    self.__Shopfloor__.clearnCrossCenterResult()
                    self.__Shopfloor__.clearnColorCheckResult()
                    
                self.__dataevent__["statusdisplay"].SetData(ParameterList.PASS, self.__Camera__.getStatusImage(resultstring))
                self.__drawevent__["drawStatus"].wait()
                self.__drawevent__["drawStatus"].clear()

            if self.__request__["quitRequest"].isSet():
                self.__request__["startRequest"].clear()
                break
