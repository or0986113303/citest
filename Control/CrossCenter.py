import cv2
import numpy as np
from Model import CrossCenter

class Control(object):
    def __init__(self, patternsize, sensorsize):
        self.__crosscentermodel__ = CrossCenter.Model()
        self.__generatePatternImage__(patternsize["X"], patternsize["Y"])
        self.__crosscentermodel__.setSensorSize(sensorsize)
        self.__crosscentermodel__.roitmp = np.ones((sensorsize[1],sensorsize[0]),np.uint8)
        self.__crosscentermodel__.element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))  
        self.__crosscentermodel__.centershiftsqeuere = {"XShift" : np.zeros(30,np.int8), "YShift" : np.zeros(30,np.int8)}
    
    def __findnearest__(self, array, value):
        #print len(array)
        idx = (np.abs(array-value)).argmin()
        return idx

    def setCenterShiftSequere(self, value, index):
        self.__crosscentermodel__.centershiftsqeuere["XShift"][index] = value["XShift"]
        #print value["X"]
        self.__crosscentermodel__.centershiftsqeuere["YShift"][index] = value["YShift"]
        #print value["Y"]
    
    def getCenterShiftValue(self):
        #print self.__crosscentermodel__.centershiftsqeuere["X"]
        #print self.__crosscentermodel__.centershiftsqeuere["Y"]
        Xhistogram = np.histogram(self.__crosscentermodel__.centershiftsqeuere["X"])
        Yhistogram = np.histogram(self.__crosscentermodel__.centershiftsqeuere["Y"])
        #print Xhistogram
        #print max(Xhistogram[0])
        #print Yhistogram
        #print max(Yhistogram[0])
        Xvalue = self.__findnearest__(Xhistogram[0], max(Xhistogram[0]))
        Yvalue = self.__findnearest__(Yhistogram[0], max(Yhistogram[0]))
        #print Xvalue
        #print Yvalue
        XShift = Xhistogram[1][Xvalue]
        YShift = Yhistogram[1][Yvalue]
        #print XShift
        #print YShift
        shiftvector = {"X" : XShift, "Y" : YShift}
        return shiftvector

    def __generatePatternImage__(self, width, height):
        tmppattern = np.zeros((width,height,1) , np.uint8)
        tmppattern[:,:] = 255
        tmppattern[0:width/2, 0:height/2] = 0
        tmppattern[width/2:width, height/2:height] = 0
        self.__crosscentermodel__.setPatternImage(tmppattern)
    
    def drawSensorCenter(self, img, width, height):
        cv2.line(img, (width/2, 0), (width/2, height),(255,0,0),2)
        cv2.line(img, (0, height/2), (width, height/2),(255,0,0),2)

    def drawResult(self, img, offset):
        cv2.circle(img,(self.__crosscentermodel__.caculatecenter["x"],self.__crosscentermodel__.caculatecenter["y"]),5,(0,255,255),-1)
        cv2.line(img, (self.__crosscentermodel__.caculatecenter["x"], 0), \
        (self.__crosscentermodel__.caculatecenter["x"], \
        self.__crosscentermodel__.getSensorSize()[1]),(0,255,255),1)
        cv2.line(img, (0, self.__crosscentermodel__.caculatecenter["y"]), \
        (self.__crosscentermodel__.getSensorSize()[0], \
        self.__crosscentermodel__.caculatecenter["y"]),(0,255,255),1)
    
    def drawColorShadeROI(self, img, ROIs, ROIsize):
        for majorkey, subdict in ROIs.iteritems():
            cv2.rectangle(img, \
            (int(subdict[0]), int(subdict[1])), \
            (int(subdict[0] + ROIsize["X"]), int(subdict[1] + ROIsize["Y"])), \
            (255,0,255), 2)

    def drawColorShadeResult(self, img, shifttable):
        cv2.line(img, (0, int(img.shape[0]/2 + shifttable["YShift"])), (img.shape[1], int(img.shape[0]/2 + shifttable["YShift"])),(0,128,255),1)
        cv2.line(img, (int(img.shape[1]/2 + shifttable["XShift"]), 0), (int(img.shape[1]/2 + shifttable["XShift"]), img.shape[0]),(0,128,255),1)
        resultstring = "(X : " + str(shifttable["XShift"]) + ", Y : " + str(shifttable["YShift"]) + ")"
        cv2.putText(img, resultstring , (int(img.shape[1]/2 + shifttable["XShift"]), \
        int(img.shape[0]/2 + shifttable["YShift"])) , cv2.FONT_HERSHEY_SIMPLEX, 1,(0,128,255), 2)

            
    def setColorShadeROIs(self, img, ROIs, ROIsize):
        for majorkey, subdict in ROIs.iteritems():
            self.__crosscentermodel__.colorshadeareasource[majorkey] = img[int(subdict[1]):int(subdict[1] + ROIsize["Y"] - 1), \
            int(subdict[0]):int(subdict[0] + ROIsize["X"] - 1)]
            self.__crosscentermodel__.colorshadeareasource[majorkey] = \
            cv2.morphologyEx(self.__crosscentermodel__.colorshadeareasource[majorkey], cv2.MORPH_OPEN, self.__crosscentermodel__.element)

    def __XDirectLocation__(self, img):
        tmp = np.zeros((img.shape[1]),np.uint8)

        for i in range(0,tmp.shape[0],1):
            tmp[i] = sum(img[:,i])
        
        result = np.nonzero(tmp)
        point = {"start" : None, "end" : None}
        if len(result[0]) > 0 :
            point["start"] = result[0][0]
            point["end"] = result[0][len(result[0]) - 1]
        else :
            point["start"] = 0
            point["end"] = 0

        return point
    
    def __YDirectLocation__(self, img):
        tmp = np.zeros((img.shape[0]),np.uint8)

        for i in range(0,tmp.shape[0],1):
            tmp[i] = sum(img[i,:])
        
        result = np.nonzero(tmp)
        point = {"start" : None, "end" : None}
        if len(result[0]) > 0 :
            point["start"] = result[0][0]
            point["end"] = result[0][len(result[0]) - 1]
        else :
            point["start"] = 0
            point["end"] = 0

        return point
    
    def __lenscornerdetecte__(self, img):
        
        XLocation = self.__XDirectLocation__(img)
        YLocation = self.__YDirectLocation__(img)

        point = {"X" : XLocation, "Y" : YLocation}

        return point

    def __shiftcaculate__(self, ROIsize, lenscorner):
        xvector = 0
        yvector = 0

        xcenter = (lenscorner["X"]["start"] + lenscorner["X"]["end"]) / 2
        
        ycenter = (lenscorner["Y"]["start"] + lenscorner["Y"]["end"]) / 2
        
        xvector = xcenter - ROIsize["X"]/2
        yvector = ycenter - ROIsize["Y"]/2
        
        vertor = {"X" : xvector, "Y" : yvector}

        return vertor
            

    def caculateColorShadeArea(self, ROIs, ROIsize):
        xvector = 0
        yvector = 0
        for majorkey, subdict in ROIs.iteritems():
            self.__crosscentermodel__.colorshadearearesult[majorkey] = \
            cv2.threshold(self.__crosscentermodel__.colorshadeareasource[majorkey],127,1,0)[1]
            self.__crosscentermodel__.colorshadelocation[majorkey] = \
            self.__lenscornerdetecte__(self.__crosscentermodel__.colorshadearearesult[majorkey])

            result = self.__shiftcaculate__(ROIsize, self.__crosscentermodel__.colorshadelocation[majorkey])

            xvector += result["X"]
            yvector += result["Y"]

        vertor = {"X" : xvector, "Y" : yvector}
        return vertor
            
    def patterndetect(self, img):
        res = cv2.matchTemplate(img,self.__crosscentermodel__.getPatternImage(),cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        tmpx = 0
        tmpy = 0
        count = 0
        for pt in zip(*loc[::-1]):
            tmpx += pt[0] + self.__crosscentermodel__.getPatternImage().shape[0]/2
            tmpy += pt[1] + self.__crosscentermodel__.getPatternImage().shape[1]/2
            count += 1
        if count == 0 :
            tmpx = 0
            tmpy = 0
        else : 
            tmpx = tmpx/count
            tmpy = tmpy/count
        self.__crosscentermodel__.setPatternPoints((tmpx,tmpy))

    def caculatecenter(self, offset):
        postion = self.__crosscentermodel__.getPatternPoints()
        if not (postion[0] == 0 and postion[1] == 0):
            self.__crosscentermodel__.caculatecenter["x"] = postion[0] + int(offset["X"])
            self.__crosscentermodel__.caculatecenter["y"] = postion[1] + int(offset["Y"])
        else :
            self.__crosscentermodel__.caculatecenter["x"] = 0
            self.__crosscentermodel__.caculatecenter["y"] = 0
    
    def getHolderLensShiftValue(self, width, height, configuration):
        if self.__crosscentermodel__.caculatecenter["x"] == 0 :
            XShift = 0
        else :
            XShift = self.__crosscentermodel__.caculatecenter["x"] - width/2 - float(configuration["FixtureXShift"])

        if self.__crosscentermodel__.caculatecenter["y"] == 0 :
            YShift = 0
        else :
            YShift = self.__crosscentermodel__.caculatecenter["y"] - height/2 - float(configuration["FixtureYShift"])

        shiftvector = {"XShift" : XShift, "YShift" : YShift}

        return shiftvector
        
    def __del__(self):
        del self.__crosscentermodel__