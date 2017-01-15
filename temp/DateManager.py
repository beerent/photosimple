import time

class DateManager(object):

    def __init__(self):
        nothing = None
    
    def getCurrentDate(self):
        return time.strftime("%Y-%m-%d")
    
    def getCurrentYear(self):
        return time.strftime("%Y")
    
    def getCurrentMonth(self):
        return time.strftime("%m")
    
    def getCurrentDay(self):
        return time.strftime("%d")