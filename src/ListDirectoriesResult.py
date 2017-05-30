class ListDirectoriesResult():
    
    def __init__(self, directories, error, successful):
        self.directories = directories
        self.error = error
        self.successful = successful
    
    def setDirectories(self, directories):
        self.directory = directory
    
    def setError(self, error):
        self.error = error
        
    def setSuccessful(self, successful):
        self.successful = successful
        
    def getDirectories(self):
        return self.directories
    
    def getError(self):
        return self.error
    
    def isSuccessful(self):
        return self.successful