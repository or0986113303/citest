import cv2
import numpy as np

from Model import ColorSpace

class Control(object):
    def __init__(self):
        self.__colormodel__ = ColorSpace.Model()

    def __del__(self):
        del self.__colormodel__
    
    def setCondition(self, value):
        #print value
        self.__colormodel__.setCondition(value)
    
    def getCondition(self, value):
        return self.__colormodel__getCondition()

    def setSourceImage(self, value):
        self.__colormodel__.setSourceImage(value)
    
    def getSourceImage(self, value):
        return self.__colormodel_getSourceImage()
    
    def __findnearest__(self, array, value):
        #print len(array)
        idx = (np.abs(array-value)).argmin()
        return idx
    
    def __judgement__(self, target, means1, means2, standarddeviation):
        result = False
        #print target
        #print target < int(means) + int(standarddeviation)
        #print target > int(means) - int(standarddeviation)
        #print type(target)
        if target < int(means1) + int(standarddeviation) and target > int(means1) - int(standarddeviation) :
            result = True
        else :
            if target < int(means2) + int(standarddeviation) and target > int(means2) - int(standarddeviation) :
                result = True
            else :
                result = False
            
        
        return result
        
    def caculatecolor(self):
        result = {"BColor" : 0, "GColor" : 0, "RColor" : 0, "Result" : None}
        passfailflag = 0
        BChannel,GChannel,RChannel = cv2.split(self.__colormodel__.getSourceImage())
        condition = self.__colormodel__.getCondition()
        #print condition

        BhistHigh,bins = np.histogram(BChannel)
        
        #print "B channel"
        #print BhistHigh
        #print max(BhistHigh)
        #print bins
        index = self.__findnearest__(BhistHigh, max(BhistHigh))
        #print index
        #print bins
        if self.__judgement__(abs(bins[index]), \
        self.__colormodel__.getCondition()["BMean1"], \
        self.__colormodel__.getCondition()["BMean2"], \
        self.__colormodel__.getCondition()["BStd"]) :
            passfailflag += 1
            result["BColor"] = 25
        else :
            result["BColor"] = bins[index]
        #if abs(bins[index]) <= self.__colormodel__.getCondition()["BMean"] + self.__colormodel__.getCondition()["BStd"] :
        #    passfailflag += 1
        
        
        #print 

        GhistHigh,bins = np.histogram(GChannel)
        
        #print "G channel"
        #print GhistHigh
        #print max(GhistHigh)
        #print bins
        index = self.__findnearest__(GhistHigh, max(GhistHigh))
        #print index
        #print bins
        if self.__judgement__(abs(bins[index]), \
        self.__colormodel__.getCondition()["GMean1"], \
        self.__colormodel__.getCondition()["GMean2"], \
        self.__colormodel__.getCondition()["GStd"]) :
            passfailflag += 1
            result["GColor"] = 25
        else :
            result["GColor"] = bins[index]
        #if abs(bins[index]) <= self.__colormodel__.getCondition()["GMean"] + self.__colormodel__.getCondition()["GStd"] :
        #    passfailflag += 1
        #print bins[index]

        

        RhistHigh,bins = np.histogram(RChannel)
        
        #print "R channel"
        #print RhistHigh
        #print max(RhistHigh)
        #print bins
        index = self.__findnearest__(RhistHigh, max(RhistHigh))
        #print index
        #print bins
        if self.__judgement__(abs(bins[index]), \
        self.__colormodel__.getCondition()["RMean1"], \
        self.__colormodel__.getCondition()["RMean2"], \
        self.__colormodel__.getCondition()["RStd"]) :
            passfailflag += 1
            result["RColor"] = 25
        else :
            result["RColor"] = bins[index]
            
        #if abs(bins[index]) <= self.__colormodel__.getCondition()["RMean"] + self.__colormodel__.getCondition()["RStd"] :
        #    passfailflag += 1
        #print bins[index]
        

        if passfailflag == 3 :
            result["Result"] = True
        else :
            result["Result"] = False
        
        return result
        