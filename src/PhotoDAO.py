#from Photo import Photo
from fileinput import filename

class PhotoDAO(object):
    
    def __init__(self, database_manager):
        self.database_manager = database_manager
        
    def getPhotoHashes(self):
        sql = "select hash from photos"
        res = self.database_manager.execute(sql, [])
        if len(res) == 0:
            return []   
        return res
    
    def backupPhoto(self, file_name, sub_directory, hash, modified, source, destination):
        sql = "insert into photos (file_name, sub_directory, hash, source, added, modified) values (%s, %s, %s, %s, now(), %s)" 
        vals = (file_name, sub_directory, hash, source.getId(), modified)
        photo_id = self.database_manager.execute(sql, vals)
        
    def getPhotosInSubDirectory(self, dir):
        sql = "select * from photos where sub_directory = %s"
        vals = (dir,)
        res = self.database_manager.execute(sql, vals)
        return res