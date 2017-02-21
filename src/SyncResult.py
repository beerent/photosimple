class SyncResult():
    
    def __init__(self, destinations, successful, error):
        self.destinations = []
        self.successful = False
        self.error = None
        
        if destinations is not None:
            for dir in destinations:
                self.addDestination(dir)

        if successful is not None:
            self.successful = successful
            
        if error is not None:
            self.error = error
    
    def addDestination(self, destination):
        self.destinations.append(destination)
    
    def getDestinations(self):
        return self.destinations
    
    def setError(self, error):
        self.error = error
        
    def getError(self):
        return self.error
    
    def setSuccessful(self, successful):
        this.successful = successful
        
    def isSuccessful(self):
        return self.successful