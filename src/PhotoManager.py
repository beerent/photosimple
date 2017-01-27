from PhotoDAO import PhotoDAO

class PhotoManager(object):
    
    def __init__(self, database_manager):
        self.photo_dao = PhotoDAO(database_manager)
                 
    def getPhotoHashes(self):
        hashes = []
        db_hashes = self.photo_dao.getPhotoHashes()
        for hash in db_hashes:
            hashes.append(hash[0])
        return hashes
