from Logger import Logger
from DirectoryDAO import DirectoryDAO
import os

class DirectoryManager():

    def __init__(self, database_manager):
        self.logger = Logger()
        self.directory_dao = DirectoryDAO(database_manager)

    def addDestination(self, directory):
        self.logger.log("attempting to add destination: %s" % directory)

        #debug
        dir_exists = self.directoryExists(directory)
        debug_str = "directory '%s' exists: %s" % (directory, str(dir_exists)) 
        self.logger.debug(debug_str)
        
        if not dir_exists:
            err_str = "directory '%s' is invalid or does not exist" % directory
            self.logger.error(err_str)
            exit(1)
            
        #check if already exists in database, if so warn
        
        
        #add to database
        return None
    
    def removeDestination(self, directory):
        self.logger.log("attempting to remove destination: %s" % directory)
        
        #check if exists in database, if not err out

        #if exists, remove
        return None
    
    def directoryExists(self, directory):
        return os.path.isdir(directory)
    
    def directoryExistsInDatabase(self, directory):
        return None