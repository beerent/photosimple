class Error():
    
    def __init__(self, request, error_msg):
        self.request = request
        self.error_msg = error_msg
        
    def getErrorMessage(self):
        return self.error_msg
    
    def getRequest(self):
        return self.request