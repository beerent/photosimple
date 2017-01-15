class DirectoryDAO(object):
    
    def __new__(self, database_manager):
        self.database_manager = database_manager
        self.database_manager.connect()