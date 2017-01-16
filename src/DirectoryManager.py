from Logger import Logger
from DirectoryDAO import DirectoryDAO
import os

class DirectoryManager():
    directory_dao = None

    def __init__(self, database_manager):
        self.logger = Logger()
        self.directory_dao = DirectoryDAO(database_manager)
        print self.directory_dao

    def addDestination(self, name, directory):
        self.logger.log("attempting to add destination: %s" % directory)

        #debug
        dir_exists = self.directoryExists(directory)
        debug_str = "directory '%s' exists: %s" % (directory, str(dir_exists)) 
        self.logger.debug(debug_str)
        
        #check if directory exists before proceeding
        if not dir_exists:
            err_str = "directory '%s' is invalid or does not exist" % directory
            self.logger.error(err_str)
            exit(1)
            
        #check if already exists in database by name, if so quit
        destination = self.directory_dao.getDestinationByName(name)
        if destination != None:
            self.logger.error("destination name '%s' already exists. Cannot continue." % name)
            return

        #check if already exists in database, if so warn
        destination = self.directory_dao.getDestinationByDirectory(directory)
        if destination != None:
            self.logger.warn("destination '%s' already exists. Doing nothing." % directory)
            return
        self.logger.debug("destination '%s' is valid and not in database" % directory)
        
        self.directory_dao.addDestination(name, directory)
        self.logger.log("destination '%s' successfully added." % directory)
        
        return None
    
    def removeDestination(self, name, directory):
        self.logger.log("attempting to remove destination: %s" % directory)
        
        #check if exists in database, if not err out

        #if exists, remove
        return None
    
    def directoryExists(self, directory):
        return os.path.isdir(directory)
    
    def directoryExistsInDatabase(self, directory):
        return None