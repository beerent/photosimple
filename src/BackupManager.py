from DirectoryManager import DirectoryManager
from DirectoryType import DirectoryType

class BackupManager(object):
    
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.directory_manager = DirectoryManager(database_manager)
            
    def backupPhotos(self):
        #for every source, backup to every destination
        type = DirectoryType("SOURCE")
        self.directory_manager.getDirectories(type)
        return None