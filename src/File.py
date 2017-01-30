class File(object):
    
    def __init__(self, name, path, modified, hash):
        self.name = name
        self.path = path
        self.modified = modified
        self.hash = hash
         
    def getName(self):
        return self.name
    
    def getPath(self):
        return self.path
    
    def getModified(self):
        return self.modified
    
    def getHash(self):
        return self.hash
