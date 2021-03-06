class Directory(object):
    directory_id = -1
    directory_path = None
    directory_type = None
    directory_name = None
    root = None
    
    
    def __init__(self, directory_id, directory_name, directory_path, directory_type, active, root):
        self.directory_id = directory_id
        self.directory_name = directory_name
        self.directory_path = directory_path
        self.directory_type = directory_type
        self.active = active
        self.root = root
         
    def getId(self):
        return self.directory_id
        
    def getName(self):
        return self.directory_name
    
    def getPath(self):
        return self.directory_path
    
    def getType(self):
        return self.directory_type
    
    def isActive(self):
        return self.active == "1"
    
    def isRoot(self):
        return self.root == "1"
    
    def __str__(self):
        ret_str = "[%s | %s | %s | %s | %s | %s]" % (str(self.directory_id), self.directory_name, self.directory_path, self.directory_type, self.active, self.root)
        return ret_str