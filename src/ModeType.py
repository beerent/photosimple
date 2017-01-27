class ModeType(object):
    mode_type = None
    
    def __init__(self, mode_type):
        if mode_type.upper() == "TODAY":
            self.mode_type = "TODAY"
        elif mode_type.upper() == "CAPTURED":
            self.mode_type = "CAPTURED"
        else:
            raise Exception("'%s' is not a valid Mode Type." % mode_type)
            
    def getModeType(self):
        return self.mode_type
        