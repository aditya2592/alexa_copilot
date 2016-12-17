__all__ = ["Payload"]

class Payload:
    deviceID = ""
    appID = ""
    ctype = ""
    cvalue = ""
    def __init__(self, deviceID, appID):
        self.deviceID = deviceID
        self.appID = appID
    def setType(self, ctype, cvalue):
        self.ctype = ctype
        self.cvalue = cvalue