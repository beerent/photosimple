import time

class DateManager(object):
    
#    def __init__(self):    
    def getDate(self):
        return time.strftime("%Y/%m/%d")
    
    def getYear(self):
        return time.strftime("%Y")
    
    def getMonth(self):
        return time.strftime("%m")
    
    def getDay(self):
        return time.strftime("%d")
    
    def getCreatedYear(self, datetime):
        return datetime.split("-")[0]
    
    def getCreatedMonth(self, datetime):
        return datetime.split("-")[1]
    
    def getCreatedDay(self, datetime):
        return datetime.split("-")[2].split(" ")[0]
        