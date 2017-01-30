from PhotoDAO import PhotoDAO
from Photo import Photo

class PhotoManager(object):
    
    def __init__(self, database_manager):
        self.photo_dao = PhotoDAO(database_manager)
                 
    def getPhotoHashes(self):
        hashes = []
        db_hashes = self.photo_dao.getPhotoHashes()
        for hash in db_hashes:
            hashes.append(hash[0])
        return hashes
    
    def getPhotosInSubDirectory(self, dir):
        result = self.photo_dao.getPhotosInSubDirectory(dir)
        
        photos = []
        for photo in result:
            #self, id, name, sub_dir, hash, source, added, modified
            photos.append(Photo(photo[0], photo[1], photo[2], photo[3], photo[4], photo[5], photo[6]))
        
        return photos