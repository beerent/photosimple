class BackupSourceResult():
    
    def __init__(self, directory, processed, backed_up, successful, error):
        self.directory = directory
        self.processed = processed
        self.backed_up = backed_up
        self.successful = successful
        self.error = error
    
    def setDirectory(self, directory):
        self.directory = directory
    
    def setProcessed(self, processed):
        self.processed = processed
        
    def setBackedUp(self, backed_up):
        self.backed_up = backed_up
        
    def getBackedUp(self):
        return self.backed_up
        
    def getDirectory(self):
        return self.directory
    
    def getProcessed(self):
        return self.processed
    
    def setSuccessful(self, successful):
        self.successful = successful
        
    def isSuccessful(self):
        return self.successful
    
    def setError(self, error):
        self.error = error
    
    def getError(self):
        return self.error