# -*- coding: utf-8 -*-

from win32api import GetSystemMetrics

import wx
import math


# Image size definitions
IMG_WIDTH = 720
IMG_HEIGHT = 480

# Buttom layout buffer size
BUTTOM_SIZE = 120

# Monitor resolution
MONITORWIDTH = GetSystemMetrics(0)
MONITORHEIGHT = GetSystemMetrics(1)

# Offset of height
HEIGHTOFFSET = MONITORHEIGHT/16

# Layout postion
if MONITORHEIGHT > 2*IMG_HEIGHT :
        CAMERAWINDOW_X = ( MONITORWIDTH - 2*IMG_WIDTH ) / 3
        CAMERAWINDOW_Y = 0
else :
        CAMERAWINDOW_X = ( MONITORWIDTH - 2*IMG_WIDTH ) / 3
        CAMERAWINDOW_Y = ( MONITORHEIGHT - 2*IMG_HEIGHT ) / 3

# Location define
LEFTTOP = "LefttopField"
LEFTBUTTON = "LeftbuttonField"
RIGHTTOP = "RighttopField"
RIGHTBUTTON = "RightbuttonField"
CENTER = "center"
PATTERN = "pattern"
MTF = "MTF"

# ROI Table
ROIW = 50
ROIH = 30
ROIXDISTANCE = 2.1*ROIW
ROIYDISTANCE = 2*ROIH 

PATTERNW = 2.5*ROIW
PATTERNH = 2*ROIH

'''
ROIs = {CENTER:[IMG_WIDTH/2 - ROIW/2 - 1.1*ROIW, IMG_HEIGHT/2 - ROIH/2], \
LEFTTOP:[IMG_WIDTH/2 - ROIXDISTANCE - ROIW/2, IMG_HEIGHT/2 - ROIYDISTANCE - ROIH/2], \
RIGHTTOP:[IMG_WIDTH/2 + ROIXDISTANCE - ROIW/2, IMG_HEIGHT/2 - ROIYDISTANCE - ROIH/2], \
LEFTBUTTON:[IMG_WIDTH/2 - ROIXDISTANCE - ROIW/2, IMG_HEIGHT/2 + ROIYDISTANCE - ROIH/2], \
RIGHTBUTTON:[IMG_WIDTH/2 + ROIXDISTANCE - ROIW/2, IMG_HEIGHT/2 + ROIYDISTANCE - ROIH/2]}

MTFTHERSHOLD = {CENTER:0.8, \
LEFTTOP:0.8, \
RIGHTTOP:0.8, \
LEFTBUTTON:0.8, \
RIGHTBUTTON:0.8}

MTFRESULT = {CENTER:"None", \
LEFTTOP:"None", \
RIGHTTOP:"None", \
LEFTBUTTON:"None", \
RIGHTBUTTON:"None"}

ROIs = {CENTER:[IMG_WIDTH/2 - ROIW/2 - ROIXDISTANCE, IMG_HEIGHT/2 - ROIH/2], \
LEFTTOP:[IMG_WIDTH/2 - ROIW/2 - ROIXDISTANCE, IMG_HEIGHT/2 - ROIH/2], \
RIGHTTOP:[IMG_WIDTH/2 - ROIW/2 + ROIXDISTANCE, IMG_HEIGHT/2 - ROIH/2], \
LEFTBUTTON:[IMG_WIDTH/2 - ROIW/2 - 2*ROIXDISTANCE, IMG_HEIGHT/2 - ROIH/2], \
RIGHTBUTTON:[IMG_WIDTH/2 - ROIW/2 + 2*ROIXDISTANCE, IMG_HEIGHT/2 - ROIH/2]}
'''

MTFTHERSHOLD = {LEFTTOP:0.8, \
RIGHTTOP:0.8, \
LEFTBUTTON:0.8, \
RIGHTBUTTON:0.8}

MTFRESULT = {LEFTTOP:"None", \
RIGHTTOP:"None", \
LEFTBUTTON:"None", \
RIGHTBUTTON:"None"}

ROIs = {LEFTTOP:[IMG_WIDTH/2 - ROIW/2 - ROIXDISTANCE, IMG_HEIGHT/2 - ROIH/2], \
RIGHTTOP:[IMG_WIDTH/2 - ROIW/2 + ROIXDISTANCE, IMG_HEIGHT/2 - ROIH/2], \
LEFTBUTTON:[IMG_WIDTH/2 - ROIW/2 - 2*ROIXDISTANCE, IMG_HEIGHT/2 - ROIH/2], \
RIGHTBUTTON:[IMG_WIDTH/2 - ROIW/2 + 2*ROIXDISTANCE, IMG_HEIGHT/2 - ROIH/2]}

PATTERNROI = {PATTERN:[IMG_WIDTH/2 - PATTERNW/2, IMG_HEIGHT/2 - PATTERNH/2]}

PATTERNOFFSETX = IMG_WIDTH/2 - PATTERNW/2
PATTERNOFFSETY = IMG_HEIGHT/2 - PATTERNH/2

PATTERNOFFSET = {"X" : PATTERNOFFSETX, "Y" : PATTERNOFFSETY}

PATTERNSIZE = {"X" : 50, "Y" : 50}

COLORSHADEROISIZE = {"X": IMG_WIDTH/10,"Y" : IMG_HEIGHT/4}

COLORSHADEROICENTER = {LEFTTOP : [0 + COLORSHADEROISIZE["X"]/2, 0 + COLORSHADEROISIZE["Y"]/2], \
RIGHTTOP : [IMG_WIDTH - COLORSHADEROISIZE["X"]/2, 0 + COLORSHADEROISIZE["Y"]/2], \
LEFTBUTTON : [0 + COLORSHADEROISIZE["X"]/2, IMG_HEIGHT - COLORSHADEROISIZE["Y"]/2], \
RIGHTBUTTON : [IMG_WIDTH - COLORSHADEROISIZE["X"]/2, IMG_HEIGHT - COLORSHADEROISIZE["Y"]/2]}

COLORSHADEREFPOINT = {LEFTTOP : [0 , 0 ], \
RIGHTTOP : [IMG_WIDTH - COLORSHADEROISIZE["X"], 0 ], \
LEFTBUTTON : [0 , IMG_HEIGHT - COLORSHADEROISIZE["Y"]], \
RIGHTBUTTON : [IMG_WIDTH - COLORSHADEROISIZE["X"], IMG_HEIGHT - COLORSHADEROISIZE["Y"]]}

MTFTHERSHOLD = {CENTER:0.7, \
LEFTTOP:0.7, \
RIGHTTOP:0.7, \
LEFTBUTTON:0.7, \
RIGHTBUTTON:0.7}

# declare camera id
CAMERAIDSTRING = "CameraID"
CAMERAID = 0

# declare environment items deinfe
PARTICLE = "Particle"

#FFTTHERSHOLD = 2000000
FFTTHERSHOLD = 2100000
# Draw line color
# ROI regatangle color
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
MAGENTA = (255,0,255)

ROICOLOR = {CENTER:RED , LEFTTOP:GREEN , RIGHTTOP:BLUE , LEFTBUTTON:YELLOW , RIGHTBUTTON:MAGENTA }

##MTFLINECOLOR = {CENTER:"-rv", LEFTTOP:"-gv" , RIGHTTOP:"-bv" , LEFTBUTTON:"-yv" , RIGHTBUTTON:"-mv"}
MTFLINECOLOR = {LEFTTOP:"-gv" , RIGHTTOP:"-bv" , LEFTBUTTON:"-yv" , RIGHTBUTTON:"-mv"}
'''
[[IMG_WIDTH*2/10 - ROIW/2 - 5, IMG_HEIGHT/2 - ROIH/2 - 10],
        [IMG_WIDTH*2/10 + ROIW/2 - 5, IMG_HEIGHT/2 + ROIH/2 - 10],
        [IMG_WIDTH*5/10 - ROIW/2 + 5, IMG_HEIGHT/2 - ROIH/2 - 10],
        [IMG_WIDTH*5/10 + ROIW/2 + 5, IMG_HEIGHT/2 + ROIH/2 - 10],
        [IMG_WIDTH*8/10 - ROIW/2 + 15, IMG_HEIGHT/2 - ROIH/2 - 10],
        [IMG_WIDTH*8/10 + ROIW/2 + 15, IMG_HEIGHT/2 + ROIH/2 - 10]]
'''
        
NUMBEROFROIS = 3

# declare serial length item define
LENGTH = "length"

# Serieal Length
SERIEALLENGTH = 13

# Self event
EVENTBINDTABLE = {"IMAGE" : wx.PyEventBinder(wx.NewEventType(), 0)\
,"DFTDATA" : wx.PyEventBinder(wx.NewEventType(), 0)\
,"MTFDATA" : wx.PyEventBinder(wx.NewEventType(), 0)\
,"STATUS" : wx.PyEventBinder(wx.NewEventType(), 0)\
,"REFLUSH" : wx.PyEventBinder(wx.NewEventType(), 0)\
,"RECORD" : wx.PyEventBinder(wx.NewEventType(), 0)\
,"CROSSCENTER" : wx.PyEventBinder(wx.NewEventType(), 0)\
,"FWCHECK" : wx.PyEventBinder(wx.NewEventType(), 0)\
,"COLORCHECK" : wx.PyEventBinder(wx.NewEventType(), 0)\
,"AMMETER" : wx.PyEventBinder(wx.NewEventType(), 0)\
,"STATUSDISPLAY" : wx.PyEventBinder(wx.NewEventType(), 0)\
,"SERIEALCHECK" : wx.PyEventBinder(wx.NewEventType(), 0)}

# Arduino comport setting
COM4 = "COM4"
BAUDRATE = 9600

# pre UI tittle
PREUITITTLE = u"設定"

# UI tittle
MAINUITITLE = "AOI with shopfloor"

# Shopfloor keys
ITEMS = "items"
TESTVALUE = "testvalue"
TESTRESULT = "testresult"

# binaryfile path
BINARYFILEPATH = "./IQsettings.BIN"

# Data event tables
DATAEVENTTABLE = {"ImageIn" : None, "DFTIn" : None, "MTFIn" : None, "Flush" : None, "Record" : None, \
"CrossCenter" : None, "fwcheck" : None, "colorcheck" : None, "ammetercheck" : None, "statusdisplay" : None, "seriealcheck" : None}

# Request tables
REQUESTTABLE = {"quitRequest" : None, "flushRequest" : None, "startRequest" : None, "pauseRequest" : None \
, "recordRequest" : None, "caculateRequest" : None, "crosscenterRequest" : None, "fwcheckRequest" : None, "colorcheckRequest" : None\
, "ammeterRequest" : None, "statusdisplayRequest" : None, "seriealRequest" : None}

# Draw event tables
DRAWEVENTTABLE = {"drawcameraview" : None, "drawDFT" : None, "drawMTF" : None, "drawStatus" : None, "drawCrossCenter" : None}

# declare sensor to pixel scale item define
SENSOR = "Sensor"
XSCALE = "XScale"
YSCALE = "YScale"

SENSORPIXELSCALE = {XSCALE : 0.5, YSCALE : 1.3}

# declare shift item define
XDIRECT = "XShift"
YDIRECT = "YShift"

# Center shift thershold
SHIFTTHERSHOLD = {XDIRECT : 18, YDIRECT : 18}

# Shift result 
SHIFTRESULT = {XDIRECT:"None", \
YDIRECT:"None"}

# declare fw version items define
FW = "FW"
#VERSION = {FWVERSION : "0.0.0"}

# declare fw verison check item define
FWVERSION = "FWVersion"

# Fireware version check
FWVERSIONCHECK = {FWVERSION : "None"}

# declare color detect item define
RCHANNEL = "RColor"
BCHANNEL = "BColor"
GCHANNEL = "GColor"

# Color detection items
RMEANS1 = "RMean1"
RMEANS2 = "RMean2"
RSTD = "RStd"
GMEANS1 = "GMean1"
GMEANS2 = "GMean2"
GSTD = "GStd"
BMEANS1 = "BMean1"
BMEANS2 = "BMean2"
BSTD = "BStd"

# Color detection condition
COLORCONDITION = {RMEANS1 : 25, RMEANS1 : 178, RSTD : 10, GMEANS1 : 25, GMEANS2 : 178, GSTD : 10, BMEANS1 : 25,BMEANS2 : 178, BSTD : 10}

# Color detection result
COLORCHECKRESULT = {RCHANNEL : "None", GCHANNEL : "None", BCHANNEL : "None"}

# Station information
SERIALNUMBER = "serialnumber"
EMPLOYEEID = "employeeID"
STATIONNAME = "stationname"
CUSTOMERSERIALNUMBER = "customerseriealnumber"
PASS = "PASS"
FAIL = "FAIL"
NONE = "None"
STATION = "Station"
CUSTOMER = "Customer"
SERIAL = "Serial"
# declare ammeter item define
AMMETERVALUE = "Power"
TYPE = "type"
VALUE = "value"
UPPERVALUE = "uppervalue"
LOWERVALUE = "lowervalue"
UNIT = "unit"
GRATION = "graduation"
OK = "OK"

# declare ammeter result
AMMETERCHECKRESULT = {AMMETERVALUE : "None"}

# declare ammeter type name
AMMETERTYPE = ["GDM-360", "GDM-396"]

# declare ammeter thershold
AMMETERTHERSHOLD = {UPPERVALUE : 50, LOWERVALUE : 100, UNIT : "V", GRATION : "m"}

#declare ammeter select
AMMETERSELECT = "Ammeter"

# declare station information
WORKINGSTATION = {SERIALNUMBER : None, EMPLOYEEID : None,\
STATIONNAME : None, CUSTOMERSERIALNUMBER : None, AMMETERSELECT : None
}

SA = "SA"
FA = "FA"

LINE = "Line"

LINEINFORMATION = {TYPE : "SA"}

# declare Fixture config items define
AMMETERPORT = "AmmeterPort"
AMMETERBAUDRATE = "AmmeterBaudRate"
FIXTUREPORT = "FixturePort"
FIXTUREBAUDRATE = "FixtureBaudRate"
FIXTUREXSHIFT = "FixtureXShift"
FIXTUREYSHIFT = "FixtureYShift"
FIXTUREZSHIFT = "FixtureZShift"
FIXTUREXROTATE = "FixtureXRotate"
FIXTUREYROTATE = "FixtureYRotate"
FIXTUREZROTATE = "FixtureZRotate"
LIGHTER1PORT = "Lighter1Port"
LIGHTER2PORT = "Lighter2Port"
LIGHTER3PORT = "Lighter3Port"
LIGHTER1BAUDRATE = "Lighter1BaudRate"
LIGHTER2BAUDRATE = "Lighter2BaudRate"
LIGHTER3BAUDRATE = "Lighter3BaudRate"
HW = "HW"
DISPLAYTIME = "DisplayTime"
WAKEUPTIME = "WakeUpTime"
CENTERMETHOD = "CenterMethod"
ERRORMESSAGE = u"錯誤!!"
LIGHTLEVEL = "LightLevel"

# declare light level Value
LIGHTVALUE = 0

# declare configure comtainer

CONFIGURE = {AMMETERPORT : "COM1", AMMETERBAUDRATE : "2400", FIXTUREPORT : "COM4", FIXTUREBAUDRATE : "9600",\
FIXTUREXSHIFT : "0", FIXTUREYSHIFT : "0", FIXTUREZSHIFT : "0", FIXTUREXROTATE : "0", FIXTUREYROTATE : "0", FIXTUREZROTATE : "0",\
LIGHTER1PORT : "unknow", LIGHTER2PORT : "unknow", LIGHTER3PORT : "unknow", LIGHTER1BAUDRATE : "unknow", LIGHTER2BAUDRATE : "unknow", LIGHTER3BAUDRATE : "unknow",\
WAKEUPTIME : "2", DISPLAYTIME : "1", CENTERMETHOD : "1"}

# Status string list
FOCUS = "Focus "
FLUSH = "Flush "
DONE = "Done"
COMPORT = "Comport "
RECORD = "Record "
ING = "ing"
I2C = "I2C "
CROSSCENTER = "Crosscenter"
DOT = "..."
FWCHECK = "FWCheck"
COLORCHECK = "ColorCheck"
AMMETERCHECK = "PowerCheck"

# declare flow control items
FLOWCONTROL = "Flow"
FWREFLUSH = "FWReflush"


# declare flow control requirement
FLOWCONTROLER = {FWCHECK : True, FWREFLUSH : True, AMMETERCHECK : True}

# process name
PROCESSNAME = "AOI.exe"