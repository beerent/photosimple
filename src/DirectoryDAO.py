from Destination import Destination

class DirectoryDAO(object):
    
    def __init__(self, database_manager):
        self.database_manager = database_manager
        
    def getDestinationByName(self, name):
        sql = "select * from directories where directory_name = %s"
        vars = (name,)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Destination(res[0], res[1], res[2], res[3])
    
    def getDestinationByDirectory(self, destination):
        sql = "select * from directories where directory_path = %s"
        vars = (destination,)
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        res = res[0]
        return Destination(res[0], res[1], res[2], res[3])
    
    def addDestination(self, name, destination):
        sql = "insert into directories (directory_name, directory_path, directory_type) "
        sql += "values (%s, %s, %s)"
        vars = (name, destination, "DESTINATION")
        result = self.database_manager.execute(sql, vars)
        print result
        
    def removeDestination(self, destination):
        return None