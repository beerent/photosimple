from PhotoDAO import PhotoDAO

class PhotoManager(object):
    
    def __init__(self, database_manager):
        self.photo_dao = PhotoDAO(database_manager)
                 
    def getPhotoHashes(self):
        return self.photo_dao.getPhotoHashes()
