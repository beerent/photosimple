class SyncDestinationResult():
    
    def __init__(self, directory, successful, error):
        self.directory = directory
        self.successful = successful
        self.error = error
        
    def setDirectory(self, directory):
        self.directory = directory
    
    def getDirectory(self):
        return self.directory
    
    def isSuccessful(self):
        return self.successful
    
    def setSuccessful(self, successful):
        self.successful = successful
    
    def getError(self):
        return self.error
    
    def setError(self, error):
        self.error = error
        
    