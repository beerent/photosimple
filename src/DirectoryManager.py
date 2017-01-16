from Logger import Logger
from DirectoryDAO import DirectoryDAO
import os

class DirectoryManager():
    directory_dao = None

    def __init__(self, database_manager):
        self.logger = Logger()
        self.directory_dao = DirectoryDAO(database_manager)

    def addDestination(self, name, directory):
        log_msg = "attempting to add destination '%s' with name '%s'" % (directory, name)
        if name == None:
            name = directory
            log_msg = "attempting to add destination '%s' with default name '%s'" % (directory, name)
            
        self.logger.log(log_msg)

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
        
    
    def removeDestination(self, name, directory):
        if directory != None and name != None:
            self.logger.log("attempting to remove destination with directory '%s' and name '%s'" % (directory, name))
            fail_string = "cannot remove destination: destination with directory '%s' and name '%s' does not exist." % (directory, name)
            debug_string = "destination with directory '%s' and name '%s' does exist." % (directory, name)

        elif directory != None and name == None:
            self.logger.log("attempting to remove destination with directory '%s'" % directory)
            fail_string = "cannot remove destination: destination with directory '%s' does not exist." % (directory)
            debug_string = "destination with directory '%s' does exist." % (directory)

        elif directory == None and name != None:
            self.logger.log("attempting to remove destination with name '%s'" % name)
            fail_string = "cannot remove destination: destination with name '%s' does not exist." % (name)
            debug_string = "destination with name '%s' does exist." % (name)

        else:
            self.logger.error("cannot remove destination: name and directory both None.")
            exit(1)
            
        destination = self.directory_dao.getDestination(directory, name)        
        if destination == None:
            self.logger.error(fail_string)
            exit(1)
        
        #destination does exist
        self.directory_dao.removeDestination(name, directory)
        self.logger.log("destination '%s' successfully removed." % directory)
            
    
    def directoryExists(self, directory):
        return os.path.isdir(directory)
    
    def directoryExistsInDatabase(self, directory):
        return None