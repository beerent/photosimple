class DirectoryType(object):
    directory_type = None
    
    def __init__(self, directory_type):
        if directory_type.upper() == "DESTINATION":
            self.directory_type = "DESTINATION"
        elif directory_type.upper() == "SOURCE":
            self.directory_type = "SOURCE"
        else:
            raise Exception("'%s' is not a valid Directory Type." % directory_type)
            
    def getDirectoryType(self):
        return self.directory_type
        