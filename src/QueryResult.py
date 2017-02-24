class QueryResult():
    
    def __init__(self, photos, successful, error):
        self.photos = []
        self.successful = False
        self.error = None
        
        if photos is not None:
            for photo in photos:
                self.addPhoto(photo)

        if successful is not None:
            self.successful = successful
            
        if error is not None:
            self.error = error
    
    def addPhoto(self, photo):
        self.photos.append(photo)
        
    def setPhotos(self, photo):
        self.photos = photo
    
    def getPhotos(self):
        return self.photos
    
    def setSuccessful(self, successful):
        this.successful = successful
        
    def isSuccessful(self):
        return self.successful

    def setError(self, error):
        self.error = error
        
    def getError(self):
        return self.error