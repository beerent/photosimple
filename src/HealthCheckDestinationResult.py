class HealthCheckDestinationResult():
    
    def __init__(self, destination, healthy, missing_photos, extra_photos, successful, error):
        self.destination = destination
        self.missing_photos = missing_photos #photo objects
        self.extra_photos   = extra_photos   #file objects
        self.healthy = healthy
        self.successful = successful
        self.error = error
        
        if self.missing_photos is None:
            self.missing_photos = []
        if self.extra_photos is None:
            self.extra_photos = []
        
        
    def setDestination(self, destination):
        self.destination = destination
        
    def getDestination(self):
        return self.destination
        
    def setMissingPhotos(self, missing_photos):
        self.missing_photos = missing_photos
    
    def getMissingPhotos(self):
        return self.missing_photos
    
    def addMissingPhoto(self, missing_photo):
        self.missing_photos.append(missing_photo)
    
    def setExtraPhotos(self, extra_photos):
        self.extra_photos = extra_photos
        
    def getExtraPhotos(self):
        return self.extra_photos
    
    def addExtraPhoto(self, extra_photo):
        self.extra_photos.append(extra_photo)
    
    def isHealthy(self):
        return self.healthy
    
    def settHealthy(self, healthy):
        self.healthy = healthy
        
        
    def isSuccessful(self):
        return self.successful
    
    def setSuccessful(self, succesful):
        self.successful = successful
    
    def getError(self):
        return self.error
    
    def setError(self, error):
        self.error = error