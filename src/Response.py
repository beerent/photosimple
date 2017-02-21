class Response():
    
    def __init__(self):
        request = None
        success = None
        message = None
        obj     = None
        
    ########################################
    def getRequest(self):
        return self.request

    def setRequest(self, request):
        self.request = request
    ########################################
        
        
    ########################################
    def getSuccess(self):
        return self.success
    
    def setSuccess(self, success):
        self.success = success
    ########################################
    
    
    ########################################
    def getMessage(self):
        return self.message
    
    def setMessage(self, message):
        self.message = message
    ########################################
    
    
    ########################################
    def getObj(self):
        return self.obj
    
    def setObj(self, obj):
        self.obj = obj
    ########################################