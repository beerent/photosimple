class Directory(object):
    directory_id = -1
    directory_path = None
    directory_type = None
    directory_name = None
    
    
    def __init__(self, directory_id, directory_name, directory_path, directory_type):
        self.directory_id = directory_id
        self.directory_name = directory_name
        self.directory_path = directory_path
        self.directory_type = directory_type
         
    def getDirectoryId(self):
        return self.directory_id
        
    def getDirectoryName(self):
        return self.directory_name
    
    def getDirectoryPath(self):
        return self.directory_path
    
    def getDirectoryType(self):
        return self.directory_type
    
    def __str__(self):
        ret_str = "[%s | %s | %s | %s]" % (str(self.directory_id), self.directory_name, self.directory_path, self.directory_type)
        return ret_str