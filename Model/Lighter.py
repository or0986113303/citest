class Model(object):
    def __init__(self, parameter):
        #print parameter
        self.lightparameter = {"lightfirst" : {"Lighter1Port" : "COM1", "Lighter1BaudRate" : 9600},\
        "lightsecend" : {"Lighter2Port" : "COM2", "Lighter2BaudRate" : 9600},\
        "lightthird" : {"Lighter3Port" : "COM3", "Lighter3BaudRate" : 9600}}
        self.lightparameter["lightfirst"]["Lighter1Port"] = parameter["Lighter1Port"]
        self.lightparameter["lightfirst"]["Lighter1BaudRate"] = int(parameter["Lighter1BaudRate"])

        self.lightparameter["lightsecend"]["Lighter2Port"] = parameter["Lighter2Port"]
        self.lightparameter["lightsecend"]["Lighter2BaudRate"] = int(parameter["Lighter2BaudRate"])

        self.lightparameter["lightthird"]["Lighter3Port"] = parameter["Lighter3Port"]
        self.lightparameter["lightthird"]["Lighter3BaudRate"] = int(parameter["Lighter3BaudRate"])

        self.leightvalue = {"lightfirst" : {"value" : 0}, "lightsecend" : {"value" : 0}, "lightthird" : {"value" : 0}}
    
    def __del__(self):
        del self.lightparameter