#from Photo import Photo
from fileinput import filename

class PhotoDAO(object):
    
    def __init__(self, database_manager):
        self.database_manager = database_manager
        
    def getPhotoHashes(self):
        sql = "select hash from photos"
        res = self.database_manager.execute(sql, [])
        if len(res) == 0:
            return None
        res = res[0]    
        return res
    
    def backupPhoto(self, file_name, hash, modified, source_id, destination_id):
        print ("Filename" + file_name)
        print ("HASH" + hash)
        print ("MOD" + modified)
        print ("SRC" + str(source_id))
        print ("DEST" + str(destination_id))