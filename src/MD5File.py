class MD5File(object):
    
    def __init__(self, path, md5):
        self.path = path
        self.md5 = md5
         
    def getPath(self, path):
        return self.path
    
    def getFile(self, md5):
        return self.md5
