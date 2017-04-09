from Directory import Directory

class DirectoryDAO(object):
    
    def __init__(self, database_manager):
        self.database_manager = database_manager
        
    ################################
    # Get Directory
    ################################
    
    # determines if name or directory are None, and 
    # calls the appropriate function based on that
    def getDirectory(self, type, name, directory):
        if name != None and directory != None:
            return self.getDirectoryByPathAndName(type, directory, name)
        elif name == None and directory != None:
            return self.getDirectoryByPath(type, directory)
        elif name != None and directory == None:
            return self.getDirectoryByName(type, name)
        
    #returns a Directory object based on directory type and name
    def getDirectoryByName(self, type, name):
        sql = "select * from directories where directory_type = %s and directory_name = %s and active = '1'"
        vars = (type, name)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Directory(res[0], res[1], res[2], res[3], res[4], res[5])
    
    #returns a Directory object based on type and path
    def getDirectoryByPath(self, type, directory):
        sql = "select * from directories where directory_type = %s and directory_path = %s and active = '1'"
        vars = (type, directory)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Directory(res[0], res[1], res[2], res[3], res[4], res[5])
    
    #returns a Directory based on type, path and name
    def getDirectoryByPathAndName(self, type, directory, name):
        sql = "select * from directories where directory_type = %s and directory_path = %s and directory_name = %s and active = '1'"
        vars = (type, directory, name)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Directory(res[0], res[1], res[2], res[3], res[4], res[5])
    
    #returns all active directories based on type
    def getDirectories(self, type):
        sql = "select * from directories where directory_type = %s and active = '1'"
        vars = (type,)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        return res
    
    #returns the root directory
    def getRootDirectory(self):
        sql = "select * from directories where root = 1"
        res = self.database_manager.execute(sql, [])
        if len(res) == 0:
            return None
        res = res[0]
        return Directory(res[0], res[1], res[2], res[3], res[4], res[5])
    
    #returns all sub directories as strings
    def getSubDirectories(self):
        sql = "select distinct sub_directory from photos"
        res = self.database_manager.execute(sql, [])
        if len(res) == 0:
            return None
        sub_directories = []
        for result in res:
            sub_directories.append(result[0])
        return sub_directories
    
    
    
    
    
    ################################
    # Remove Directory
    ################################
    
    def removeDirectory(self, type, name, directory):
        if name != None and directory != None:
            return self.removeDirectoryByPathAndName(type, directory, name)
        elif name == None and directory != None:
            return self.removeDirectoryByPath(type, directory)
        elif name != None and directory == None:
            return self.removeDirectoryByName(type, name)
        
    def removeDirectoryByName(self, type, name):
        sql = "update directories set active = '0' where directory_type = %s and directory_name = %s and active = '1'"
        vars = (type, name)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Directory(res[0], res[1], res[2], res[3], res[4], res[5])
    
    def removeDirectoryByPath(self, type, directory):
        sql = "update directories set active = '0' where directory_type = %s and directory_path = %s and active = '1'"
        vars = (type, directory)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Directory(res[0], res[1], res[2], res[3], res[4], res[5])
    
    def removeDirectoryByPathAndName(self, type, directory, name):
        sql = "update directories set active = '0' where directory_type = %s and directory_path = %s and directory_name = %s and active = '1'"
        vars = (type, directory, name)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Directory(res[0], res[1], res[2], res[3], res[4], res[5]) 
    
    
    
    
    
    
    
    
    ################################
    # Add Directory
    ################################
    
    def addDirectory(self, type, name, directory):
        sql = "insert into directories (directory_type, directory_name, directory_path) "
        sql += "values (%s, %s, %s) on duplicate key update active = '1', directory_name = %s"
        vars = (type, name, directory, name)
        result = self.database_manager.execute(sql, vars)
        
