class Photo(object):
    
    def __init__(self, id, name, sub_dir, hash, source, added, modified):
        self.id = id
        self.name = name
        self.sub_dir = sub_dir
        self.hash = hash
        self.source = source
        self.added = added
        self.modified = modified
         
    def getId(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def getSubDirectory(self):
        return self.sub_dir

    def getHash(self):
        return self.hash

    def getSourceId(self):
        return self.source

    def getAdded(self):
        return self.added
        
    def getModified(self):
        return self.modified
