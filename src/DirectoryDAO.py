from Destination import Destination

class DirectoryDAO(object):
    
    def __init__(self, database_manager):
        self.database_manager = database_manager
        
        
        
        
        
    ################################
    # Get Destination
    ################################
    
    def getDestination(self, name, directory):
        if name != None and directory != None:
            return self.getDestinationByDirectoryAndName(directory, name)
        elif name == None and directory != None:
            return self.getDestinationByDirectory(directory)
        elif name != None and directory == None:
            return self.getDestinationByName(name)
        
    def getDestinationByName(self, name):
        sql = "select * from directories where directory_name = %s and active = '1'"
        vars = (name,)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Destination(res[0], res[1], res[2], res[3])
    
    def getDestinationByDirectory(self, directory):
        sql = "select * from directories where directory_path = %s and active = '1'"
        vars = (directory,)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Destination(res[0], res[1], res[2], res[3])
    
    def getDestinationByDirectoryAndName(self, directory, name):
        sql = "select * from directories where directory_path = %s and directory_name = %s and active = '1'"
        vars = (directory, name)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Destination(res[0], res[1], res[2], res[3])
    
    
    
    
    
    ################################
    # Remove Destination
    ################################
    
    def removeDestination(self, name, directory):
        if name != None and directory != None:
            return self.removeDestinationByDirectoryAndName(directory, name)
        elif name == None and directory != None:
            return self.removeDestinationByDirectory(directory)
        elif name != None and directory == None:
            return self.removeDestinationByName(name)
        
    def removeDestinationByName(self, name):
        sql = "update directories set active = '0' where directory_name = %s and active = '1'"
        vars = (name,)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Destination(res[0], res[1], res[2], res[3])
    
    def removeDestinationByDirectory(self, directory):
        sql = "update directories set active = '0' where directory_path = %s and active = '1'"
        vars = (directory,)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Destination(res[0], res[1], res[2], res[3])
    
    def removeDestinationByDirectoryAndName(self, directory, name):
        sql = "update directories set active = '0' where directory_path = %s and directory_name = %s and active = '1'"
        vars = (directory, name)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Destination(res[0], res[1], res[2], res[3]) 
    
    
    
    
    
    
    
    
    ################################
    # Add Destination
    ################################
    
    def addDestination(self, name, destination):
        sql = "insert into directories (directory_name, directory_path, directory_type) "
        sql += "values (%s, %s, %s) on duplicate key update active = '1', directory_name = %s"
        vars = (name, destination, "DESTINATION", name)
        result = self.database_manager.execute(sql, vars)
        
