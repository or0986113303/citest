# -*- coding: utf-8 -*-

import wx
import threading

from Model import ParameterList

class ImageIn:
    """
    Interface for sending images to the wx application.
    """
    def __init__(self, parent):
        self.parent = parent
        self.eventLock = threading.Lock()

    def SetData(self, arr, status, checkstatus):
        #create a wx.Image from the array
        h,w = arr.shape[0], arr.shape[1]

        #Format numpy array data for use with wx Image in RGB
        img = wx.ImageFromBuffer(w, h, arr)
        
        #Format numpy array data for use with wx Image in RGB
        statusimg = wx.ImageFromBuffer(w, h, status)
        #Create the event
        event = ImageEvent()
        event.img = img
        event.statusimg = statusimg
        event.status = checkstatus
        event.eventLock = self.eventLock

        #Trigger the event when app releases the eventLock
        event.eventLock.acquire() #wait until the event lock is released
        #print self.parent
        self.parent.AddPendingEvent(event)
        
# For video support
#----------------------------------------------------------------------
class ImageEvent(wx.PyCommandEvent):
    def __init__(self, eventType=ParameterList.EVENTBINDTABLE["IMAGE"].evtType[0], id=0):
        wx.PyCommandEvent.__init__(self, eventType, id)

        self.img = None
        self.statusimg = None
        self.status = None
        self.oldImageLock = None
        self.eventLock = None
#----------------------------------------------------------------------

class DFTIn:
    """
    Interface for sending graphs to the wx application.
    """
    def __init__(self, parent):
        self.parent = parent
        self.eventLock = threading.Lock()

    def SetData(self, arr):
        #create a wx.Image from the array
        h,w = arr.shape[0], arr.shape[1]

        #Format numpy array data for use with wx Image in RGB
        graph = wx.ImageFromBuffer(w, h, arr)
        
        #Create the event
        event = DFTEvent()
        event.graph = graph
        event.eventLock = self.eventLock

        #Trigger the event when app releases the eventLock
        event.eventLock.acquire() #wait until the event lock is released
        #print self.parent
        self.parent.AddPendingEvent(event)
# For video support
#----------------------------------------------------------------------
class DFTEvent(wx.PyCommandEvent):
    def __init__(self, eventType=ParameterList.EVENTBINDTABLE["DFTDATA"].evtType[0], id=1):
        wx.PyCommandEvent.__init__(self, eventType, id)

        self.graph = None
        self.oldImageLock = None
        self.eventLock = None
#----------------------------------------------------------------------

class MTFIn:
    """
    Interface for sending plot data to the wx application.
    """
    def __init__(self, parent):
        self.parent = parent
        self.eventLock = threading.Lock()

    def SetData(self, MTF, IX, POLY, Status):
        #Create the event
        event = MTFEvent()
        event.mtf = MTF
        event.ix = IX
        event.poly = POLY
        event.status = Status
        event.eventLock = self.eventLock

        #Trigger the event when app releases the eventLock
        event.eventLock.acquire() #wait until the event lock is released
        #print self.parent
        self.parent.AddPendingEvent(event)
# For video support
#----------------------------------------------------------------------
class MTFEvent(wx.PyCommandEvent):
    def __init__(self, eventType=ParameterList.EVENTBINDTABLE["MTFDATA"].evtType[0], id=1):
        wx.PyCommandEvent.__init__(self, eventType, id)

        self.mtf = None
        self.ix = None
        self.poly = None
        self.status = None
        self.oldImageLock = None
        self.eventLock = None
#----------------------------------------------------------------------


class StatusIn:
    """
    Interface for sending graphs to the wx application.
    """
    def __init__(self, parent):
        self.parent = parent
        self.eventLock = threading.Lock()

    def SetData(self, arr):
        #create a wx.Image from the array
        h,w = arr.shape[0], arr.shape[1]

        #Format numpy array data for use with wx Image in RGB
        graph = wx.ImageFromBuffer(w, h, arr)
        
        #Create the event
        event = StatusEvent()
        event.graph = graph
        event.eventLock = self.eventLock

        #Trigger the event when app releases the eventLock
        event.eventLock.acquire() #wait until the event lock is released
        #print self.parent
        self.parent.AddPendingEvent(event)
# For video support
#----------------------------------------------------------------------
class StatusEvent(wx.PyCommandEvent):
    def __init__(self, eventType=ParameterList.EVENTBINDTABLE["STATUS"].evtType[0], id=1):
        wx.PyCommandEvent.__init__(self, eventType, id)

        self.graph = None
        self.oldImageLock = None
        self.eventLock = None
#----------------------------------------------------------------------

class FlushDone:
    """
    Interface for sending plot data to the wx application.
    """
    def __init__(self, parent):
        self.parent = parent
        self.eventLock = threading.Lock()

    def SetData(self, status, arr):
        #create a wx.Image from the array
        h,w = arr.shape[0], arr.shape[1]

        #Format numpy array data for use with wx Image in RGB
        graph = wx.ImageFromBuffer(w, h, arr)
        #Create the event
        event = FlushEvent()
        event.status = status
        event.graph = graph
        event.eventLock = self.eventLock

        #Trigger the event when app releases the eventLock
        event.eventLock.acquire() #wait until the event lock is released
        #print self.parent
        self.parent.AddPendingEvent(event)

# For main process flow support
#----------------------------------------------------------------------
class FlushEvent(wx.PyCommandEvent):
    def __init__(self, eventType=ParameterList.EVENTBINDTABLE["REFLUSH"].evtType[0], id=2):
        wx.PyCommandEvent.__init__(self, eventType, id)

        self.status = None
        self.graph = None
        self.oldImageLock = None
        self.eventLock = None
#----------------------------------------------------------------------

class RecordDone:
    """
    Interface for sending plot data to the wx application.
    """
    def __init__(self, parent):
        self.parent = parent
        self.eventLock = threading.Lock()

    def SetData(self, status, arr):
        #create a wx.Image from the array
        h,w = arr.shape[0], arr.shape[1]

        #Format numpy array data for use with wx Image in RGB
        graph = wx.ImageFromBuffer(w, h, arr)
        #Create the event
        event = RecordEvent()
        event.status = status
        event.graph = graph
        event.eventLock = self.eventLock

        #Trigger the event when app releases the eventLock
        event.eventLock.acquire() #wait until the event lock is released
        #print self.parent
        self.parent.AddPendingEvent(event)

# For main process flow support
#----------------------------------------------------------------------
class RecordEvent(wx.PyCommandEvent):
    def __init__(self, eventType=ParameterList.EVENTBINDTABLE["RECORD"].evtType[0], id=2):
        wx.PyCommandEvent.__init__(self, eventType, id)

        self.status = None
        self.graph = None
        self.oldImageLock = None
        self.eventLock = None
#----------------------------------------------------------------------

class CrossCenterIn:
    """
    Interface for sending plot data to the wx application.
    """
    def __init__(self, parent):
        self.parent = parent
        self.eventLock = threading.Lock()

    def SetData(self, arr, status, checkstatus):
        #create a wx.Image from the array
        h,w = arr.shape[0], arr.shape[1]

        #Format numpy array data for use with wx Image in RGB
        img = wx.ImageFromBuffer(w, h, arr)
        
        #Format numpy array data for use with wx Image in RGB
        statusimg = wx.ImageFromBuffer(w, h, status)
        #Create the event
        event = CrossCenterEvent()
        event.img = img
        event.statusimg = statusimg
        event.status = checkstatus
        event.eventLock = self.eventLock

        #Trigger the event when app releases the eventLock
        event.eventLock.acquire() #wait until the event lock is released
        #print self.parent
        self.parent.AddPendingEvent(event)

# For main process flow support
#----------------------------------------------------------------------
class CrossCenterEvent(wx.PyCommandEvent):
    def __init__(self, eventType=ParameterList.EVENTBINDTABLE["CROSSCENTER"].evtType[0], id=3):
        wx.PyCommandEvent.__init__(self, eventType, id)

        self.img = None
        self.statusimg = None
        self.status = None
        self.oldImageLock = None
        self.eventLock = None
#----------------------------------------------------------------------

class FWCheckDone:
    """
    Interface for sending plot data to the wx application.
    """
    def __init__(self, parent):
        self.parent = parent
        self.eventLock = threading.Lock()

    def SetData(self, status, arr):
        #create a wx.Image from the array
        h,w = arr.shape[0], arr.shape[1]

        #Format numpy array data for use with wx Image in RGB
        graph = wx.ImageFromBuffer(w, h, arr)
        #Create the event
        event = FWCheckEvent()
        event.status = status
        event.graph = graph
        event.eventLock = self.eventLock

        #Trigger the event when app releases the eventLock
        event.eventLock.acquire() #wait until the event lock is released
        #print self.parent
        self.parent.AddPendingEvent(event)

# For main process flow support
#----------------------------------------------------------------------
class FWCheckEvent(wx.PyCommandEvent):
    def __init__(self, eventType=ParameterList.EVENTBINDTABLE["FWCHECK"].evtType[0], id=2):
        wx.PyCommandEvent.__init__(self, eventType, id)

        self.status = None
        self.graph = None
        self.oldImageLock = None
        self.eventLock = None
    
#----------------------------------------------------------------------

class ColorCheckDone:
    """
    Interface for sending plot data to the wx application.
    """
    def __init__(self, parent):
        self.parent = parent
        self.eventLock = threading.Lock()

    def SetData(self, status, arr, img):
        #create a wx.Image from the array
        h,w = arr.shape[0], arr.shape[1]

        #Format numpy array data for use with wx Image in RGB
        graph = wx.ImageFromBuffer(w, h, arr)
        image = wx.ImageFromBuffer(w, h, img)
        #Create the event
        event = ColorCheckEvent()
        event.status = status
        event.img = image
        event.graph = graph
        event.eventLock = self.eventLock

        #Trigger the event when app releases the eventLock
        event.eventLock.acquire() #wait until the event lock is released
        #print self.parent
        self.parent.AddPendingEvent(event)

# For main process flow support
#----------------------------------------------------------------------
class ColorCheckEvent(wx.PyCommandEvent):
    def __init__(self, eventType=ParameterList.EVENTBINDTABLE["COLORCHECK"].evtType[0], id=2):
        wx.PyCommandEvent.__init__(self, eventType, id)

        self.status = None
        self.graph = None
        self.img = None
        self.oldImageLock = None
        self.eventLock = None

#----------------------------------------------------------------------

class AmmeterCheckDone:
    """
    Interface for sending plot data to the wx application.
    """
    def __init__(self, parent):
        self.parent = parent
        self.eventLock = threading.Lock()

    def SetData(self, status, arr):
        #create a wx.Image from the array
        h,w = arr.shape[0], arr.shape[1]

        #Format numpy array data for use with wx Image in RGB
        graph = wx.ImageFromBuffer(w, h, arr)
        #Create the event
        event = AmmeterCheckEvent()
        event.status = status
        event.graph = graph
        event.eventLock = self.eventLock

        #Trigger the event when app releases the eventLock
        event.eventLock.acquire() #wait until the event lock is released
        #print self.parent
        self.parent.AddPendingEvent(event)

# For main process flow support
#----------------------------------------------------------------------
class AmmeterCheckEvent(wx.PyCommandEvent):
    def __init__(self, eventType=ParameterList.EVENTBINDTABLE["AMMETER"].evtType[0], id=2):
        wx.PyCommandEvent.__init__(self, eventType, id)

        self.status = None
        self.graph = None
        self.oldImageLock = None
        self.eventLock = None
    
#----------------------------------------------------------------------

class StatusDisplay:
    """
    Interface for sending plot data to the wx application.
    """
    def __init__(self, parent):
        self.parent = parent
        self.eventLock = threading.Lock()

    def SetData(self, status, arr):
        #create a wx.Image from the array
        h,w = arr.shape[0], arr.shape[1]

        #Format numpy array data for use with wx Image in RGB
        graph = wx.ImageFromBuffer(w, h, arr)
        #Create the event
        event = StatusDisplayEvent()
        event.status = status
        event.graph = graph
        event.eventLock = self.eventLock

        #Trigger the event when app releases the eventLock
        event.eventLock.acquire() #wait until the event lock is released
        #print self.parent
        self.parent.AddPendingEvent(event)

# For main process flow support
#----------------------------------------------------------------------
class StatusDisplayEvent(wx.PyCommandEvent):
    def __init__(self, eventType=ParameterList.EVENTBINDTABLE["STATUSDISPLAY"].evtType[0], id=2):
        wx.PyCommandEvent.__init__(self, eventType, id)

        self.status = None
        self.graph = None
        self.oldImageLock = None
        self.eventLock = None

#----------------------------------------------------------------------

class SeriealCheck:
    """
    Interface for sending plot data to the wx application.
    """
    def __init__(self, parent):
        self.parent = parent
        self.eventLock = threading.Lock()

    def SetData(self, status, arr):
        #create a wx.Image from the array
        h,w = arr.shape[0], arr.shape[1]

        #Format numpy array data for use with wx Image in RGB
        graph = wx.ImageFromBuffer(w, h, arr)
        #Create the event
        event = SeriealCheckEvent()
        event.status = status
        event.graph = graph
        event.eventLock = self.eventLock

        #Trigger the event when app releases the eventLock
        event.eventLock.acquire() #wait until the event lock is released
        #print self.parent
        self.parent.AddPendingEvent(event)

# For main process flow support
#----------------------------------------------------------------------
class SeriealCheckEvent(wx.PyCommandEvent):
    def __init__(self, eventType=ParameterList.EVENTBINDTABLE["SERIEALCHECK"].evtType[0], id=2):
        wx.PyCommandEvent.__init__(self, eventType, id)

        self.status = None
        self.graph = None
        self.oldImageLock = None
        self.eventLock = None