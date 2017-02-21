class DirectoryResult():
    
    def __init__(self, directory, error, successful):
        self.directory = directory
        self.error = error
        self.successful = successful
    
    def setDirectory(self, directory):
        self.directory = directory
    
    def setError(self, error):
        self.error = error
        
    def setSuccessful(self, successful):
        self.successful = successful
        
    def getDirectory(self):
        return self.directory
    
    def getError(self):
        return self.error
    
    def isSuccessful(self):
        return self.successful