class MD5File(object):
    
    def __init__(self, name, path, modified, md5):
        self.name = name
        self.path = path
        self.modified = modified
        self.md5 = md5
         
    def getName(self):
        return self.name
    
    def getPath(self):
        return self.path
    
    def getModified(self):
        return self.modified
    
    def getHash(self):
        return self.md5
