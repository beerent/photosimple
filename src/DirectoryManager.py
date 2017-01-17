from Logger import Logger
from DirectoryDAO import DirectoryDAO
import os

class DirectoryManager():
    directory_dao = None

    def __init__(self, database_manager):
        self.logger = Logger()
        self.directory_dao = DirectoryDAO(database_manager)
        
        
        
    
    def addDirectory(self, type, name, directory):
        log_msg = "attempting to add %s '%s' with name '%s'" % (type.getDirectoryType(), directory, name)
        if name == None:
            name = directory
            log_msg = "attempting to add %s '%s' with default name '%s'" % (type.getDirectoryType(), directory, name)
            
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

        directory_path = self.directory_dao.getDirectoryByName(type.getDirectoryType(), name)
        if directory_path != None:
            self.logger.error("%s name '%s' already exists. Cannot continue." % (type.getDirectoryType(), name))
            return
        
        #check if already exists in database, if so warn
        directory_path = self.directory_dao.getDirectoryByDirectory(type.getDirectoryType(), directory)
        if directory_path != None:
            self.logger.warn("%s '%s' already exists. Doing nothing." % (type.getDirectoryType(), directory))
            return
        self.logger.debug("%s '%s' is valid and not in database" % (type.getDirectoryType(), directory))
        
        self.directory_dao.addDirectory(type.getDirectoryType(), name, directory)
        self.logger.log("%s '%s' successfully added." % (type.getDirectoryType(), directory))


    
    def removeDirectory(self, type, name, directory):
        if directory != None and name != None:
            self.logger.log("attempting to remove %s with directory '%s' and name '%s'" % (type.getDirectoryType(), directory, name))
            fail_string = "cannot remove %s: directory '%s' and name '%s' does not exist." % (type.getDirectoryType(), directory, name)
            debug_string = "%s with directory '%s' with name '%s' does exist." % (type.getDirectoryType(), directory, name)

        elif directory != None and name == None:
            self.logger.log("attempting to remove %s with directory '%s'" % (type.getDirectoryType(), directory))
            fail_string = "cannot remove %s: directory '%s' does not exist." % (type.getDirectoryType(), directory)
            debug_string = "%s with directory '%s' does exist." % (type.getDirectoryType(), directory)

        elif directory == None and name != None:
            self.logger.log("attempting to remove %s with name '%s'" % (type.getDirectoryType(), name))
            fail_string = "cannot remove %s: name '%s' does not exist." % (type.getDirectoryType(), name)
            debug_string = "%s with name '%s' does exist." % (type.getDirectoryType(), name)

        else:
            self.logger.error("cannot remove %s: name and directory are both None." % type.getDirectoryType())
            exit(1)
            
        directory_path = self.directory_dao.getDirectory(type.getDirectoryType(), name, directory)        
        if directory_path == None:
            self.logger.error(fail_string)
            exit(1)
        
        #destination does exist
        self.directory_dao.removeDirectory(type.getDirectoryType(), name, directory)
        self.logger.log("destination '%s' successfully removed." % directory)
            
    
    def directoryExists(self, directory):
        return os.path.isdir(directory)
    
    def directoryExistsInDatabase(self, directory):
        return None