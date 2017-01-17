from Directory import Directory

class DirectoryDAO(object):
    
    def __init__(self, database_manager):
        self.database_manager = database_manager
        
    ################################
    # Get Directory
    ################################
    
    def getDirectory(self, type, name, directory):
        if name != None and directory != None:
            return self.getDirectoryByDirectoryAndName(type, directory, name)
        elif name == None and directory != None:
            return self.getDirectoryByDirectory(type, directory)
        elif name != None and directory == None:
            return self.getDirectoryByName(type, name)
        
    def getDirectoryByName(self, type, name):
        sql = "select * from directories where directory_type = %s and directory_name = %s and active = '1'"
        vars = (type, name)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Directory(res[0], res[1], res[2], res[3])
    
    def getDirectoryByDirectory(self, type, directory):
        sql = "select * from directories where directory_type = %s and directory_path = %s and active = '1'"
        vars = (type, directory)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Directory(res[0], res[1], res[2], res[3])
    
    def getDirectoryByDirectoryAndName(self, type, directory, name):
        sql = "select * from directories where directory_type = %s and directory_path = %s and directory_name = %s and active = '1'"
        vars = (type, directory, name)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Directory(res[0], res[1], res[2], res[3])
    
    
    
    
    
    ################################
    # Remove Directory
    ################################
    
    def removeDirectory(self, type, name, directory):
        if name != None and directory != None:
            return self.removeDirectoryByDirectoryAndName(type, directory, name)
        elif name == None and directory != None:
            return self.removeDirectoryByDirectory(type, directory)
        elif name != None and directory == None:
            return self.removeDirectoryByName(type, name)
        
    def removeDirectoryByName(self, type, name):
        sql = "update directories set active = '0' where directory_type = %s and directory_name = %s and active = '1'"
        vars = (type, name)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Directory(res[0], res[1], res[2], res[3])
    
    def removeDirectoryByDirectory(self, type, directory):
        sql = "update directories set active = '0' where directory_type = %s and directory_path = %s and active = '1'"
        vars = (type, directory)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Directory(res[0], res[1], res[2], res[3])
    
    def removeDirectoryByDirectoryAndName(self, type, directory, name):
        sql = "update directories set active = '0' where directory_type = %s and directory_path = %s and directory_name = %s and active = '1'"
        vars = (type, directory, name)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Directory(res[0], res[1], res[2], res[3]) 
    
    
    
    
    
    
    
    
    ################################
    # Add Directory
    ################################
    
    def addDirectory(self, type, name, directory):
        sql = "insert into directories (directory_type, directory_name, directory_path) "
        sql += "values (%s, %s, %s) on duplicate key update active = '1', directory_name = %s"
        vars = (type, name, directory, name)
        result = self.database_manager.execute(sql, vars)
        
