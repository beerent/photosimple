from Logger import Logger
from DirectoryType import DirectoryType
from DirectoryDAO import DirectoryDAO
from DateManager import DateManager
from Directory import Directory
import os
from scipy.constants.constants import year

class DirectoryManager():
    directory_dao = None

    def __init__(self, database_manager):
        self.logger = Logger()
        self.directory_dao = DirectoryDAO(database_manager)
        self.date_manager = DateManager()
        
        
        
        
    ##########################
    # ADD DIRECTORY
    ##########################
    def addDirectory(self, type, name, directory):
        #ensure directory has a trailing '/'
        if directory[-1:] != "/":
            directory = directory + "/"
            
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
        directory_path = self.directory_dao.getDirectoryByPath(type.getDirectoryType(), directory)
        if directory_path != None:
            self.logger.warn("%s '%s' already exists. Doing nothing." % (type.getDirectoryType(), directory))
            return
        self.logger.debug("%s '%s' is valid and not in database" % (type.getDirectoryType(), directory))
        
        self.directory_dao.addDirectory(type.getDirectoryType(), name, directory)
        self.logger.log("%s '%s' successfully added." % (type.getDirectoryType(), directory))




    ##########################
    # REMOVE DIRECTORY
    ##########################  
    def removeDirectory(self, type, name, directory):
        if directory != None and name != None:
            self.logger.log("attempting to remove %s with directory '%s' and name '%s'" % (type.getDirectoryType(), directory, name))
            fail_string = "cannot remove %s: directory '%s' and name '%s' does not exist." % (type.getDirectoryType(), directory, name)
            debug_string = "removeDirectory(): %s with directory '%s' with name '%s' exists." % (type.getDirectoryType(), directory, name)

        elif directory != None and name == None:
            self.logger.log("attempting to remove %s with directory '%s'" % (type.getDirectoryType(), directory))
            fail_string = "cannot remove %s: directory '%s' does not exist." % (type.getDirectoryType(), directory)
            debug_string = "removeDirectory(): %s with directory '%s' exists." % (type.getDirectoryType(), directory)

        elif directory == None and name != None:
            self.logger.log("attempting to remove %s with name '%s'" % (type.getDirectoryType(), name))
            fail_string = "cannot remove %s: name '%s' does not exist." % (type.getDirectoryType(), name)
            debug_string = "removeDirectory(): %s with name '%s' exists." % (type.getDirectoryType(), name)

        else:
            self.logger.error("cannot remove %s: name and directory are both None." % type.getDirectoryType())
            exit(1)
            
        directory_path = self.directory_dao.getDirectory(type.getDirectoryType(), name, directory)        
        if directory_path == None:
            self.logger.error(fail_string)
            exit(1)
        self.logger.debug(debug_string)
        
        #destination does exist
        self.directory_dao.removeDirectory(type.getDirectoryType(), name, directory)
        self.logger.log("%s directory '%s' successfully removed." % (type.getDirectoryType(), directory))
    
    
    
    
        
    ##########################
    # GET DIRECTORY
    ##########################
    def getDirectories(self, type, name, directory):
        if directory != None and name != None:
            self.logger.log("attempting to get %s with directory '%s' and name '%s'" % (type.getDirectoryType(), directory, name))
            fail_string = "cannot get %s: directory '%s' and name '%s' does not exist." % (type.getDirectoryType(), directory, name)
            success_string = "successfully found %s directory with name '%s' and path '%s'" % () (type.getDirectoryType(), directory, name)
            debug_string = "getDirectory(): %s with directory '%s' with name '%s' does exist." % (type.getDirectoryType(), directory, name)

        elif directory != None and name == None:
            self.logger.log("attempting to get %s with directory '%s'" % (type.getDirectoryType(), directory))
            fail_string = "cannot get %s: directory '%s' does not exist." % (type.getDirectoryType(), directory)
            success_string = "successfully found %s directory with path '%s'" % () (type.getDirectoryType(), directory)
            debug_string = "getDirectory(): %s with directory '%s' does exist." % (type.getDirectoryType(), directory)

        elif directory == None and name != None:
            self.logger.log("attempting to get %s with name '%s'" % (type.getDirectoryType(), name))
            fail_string = "cannot get %s: name '%s' does not exist." % (type.getDirectoryType(), name)
            success_string = "successfully found %s directory with name '%s'" % () (type.getDirectoryType(), name)
            debug_string = "getDirectory(): %s with name '%s' does exist." % (type.getDirectoryType(), name)

        else:
            self.logger.error("cannot get %s: name and directory are both None." % type.getDirectoryType())
            exit(1)
            
        directory_obj = self.directory_dao.getDirectory(type.getDirectoryType(), name, directory)        
        if directory_obj == None:
            self.logger.error(fail_string)
            exit(1)
        
        self.logger.debug(success_string)
        #destination does exist
        
        dir = Directory(directory_obj[0], directory_obj[1], directory_obj[2], directory_obj[3], directory_obj[4])
        self.logger.debug("directory found: %s" % str(dir))
        return dir



    ##########################
    # GET PRESENT DIRECTORIES
    ##########################
    def getPresentDirectories(self):
        present_source_directories = []
        source_directories = self.getDirectories(DirectoryType("SOURCE"))
        for source_directory in source_directories:
            if not self.directoryExists(source_directory.getDirectoryPath()):
                self.logger.debug("source '%s' does not exist or is not accessible" % source_directory.getDirectoryName())
                continue
            self.logger.debug("source '%s' is present and accessible." % source_directory.getDirectoryName())
            present_source_directories.append(source_directory)
        return present_source_directories
        
        
    ##########################
    # GET DIRECTORIES
    ##########################
    def getDirectories(self, type):
        self.logger.debug("attempting to get all %s directories" % type.getDirectoryType())
            
        directory_objs = self.directory_dao.getDirectories(type.getDirectoryType())        
        if directory_objs == None:
            self.logger.error("no %s directories found." % type.getDirectoryType())
            exit(1)
        
        #destination does exist
        self.logger.debug("%s directories successfully found." % type.getDirectoryType())
        
        directories = []
        for directory_obj in directory_objs:
            directories.append(Directory(directory_obj[0], directory_obj[1], directory_obj[2], directory_obj[3], directory_obj[4], directory_obj[5]))
        
        for directory in directories:
            self.logger.log("%s: %s" % (type.getDirectoryType(), directory.getDirectoryPath()))
            
        self.logger.debug("%s directories found: %s" % (type.getDirectoryType(), self.directoriesToString(directories)))

        return directories
    

    ##########################
    # GET ROOT DIRECTORY
    ##########################
    def getRootDirectory(self):
        self.logger.debug("attempting to get root directory")
        directory = self.directory_dao.getRootDirectory()
        if directory == None:
            self.logger.error("No root directory found, critical error.")
            exit(1)
        self.logger.debug("directory found: %s" % str(directory))
        return directory
    
    def getSubDirectories(self):
        self.logger.debug("attempting to get all sub directories")
        results = self.directory_dao.getSubDirectories()
        
        sub_directories = []
        for result in results:
            self.logger.debug("found subdirectory: %s" % result)
            sub_directories.append(result)
        
        return sub_directories


    ##########################
    # CREATE DIRECTORY
    ##########################    
    
    def createTodaysDirectory(self, destination):
        year = self.date_manager.getYear()
        month = self.date_manager.getMonth()
        day = self.date_manager.getDay()
        self.createDateDirectory(year, month, day, destination)
        sub_dir = year + "/" + month + "/" + day + "/"
        return sub_dir
    
    
    def createModifiedDirectory(self, file, destination):
        modified_date = file.getModified()
        year = self.date_manager.getCreatedYear(modified_date)
        month = self.date_manager.getCreatedMonth(modified_date)
        day = self.date_manager.getCreatedDay(modified_date)
        self.createDateDirectory(year, month, day, destination)   
        sub_dir = year + "/" + month + "/" + day + "/"
        return sub_dir
    
                
    def createDateDirectory(self, year, month, day, destination):
        destination_path = destination.getDirectoryPath()
        self.logger.debug("creating directory %s%s/%s/%s" % (destination_path, year, month, day))
        root = destination_path

        year = root + year
        if not os.path.exists(year):
            os.system("mkdir %s" % year)
            self.logger.log("creating directory: '%s'" % year)

        month = year + "/" + month
        if not os.path.exists(month):
            os.system("mkdir %s" % month)
            self.logger.log("creating directory: '%s'" % month)
            
        day = month + "/" + day
        if not os.path.exists(day):
            os.system("mkdir %s" % day)
            self.logger.log("creating directory: '%s'" % day)
    
    def directoriesToString(self, directories):
        ret_str = ""
        for directory in directories:
            ret_str = ret_str + "\n" + str(directory) 
        return ret_str
    
#    def getDirectoryObject(self, database_obj):
#        return Directory()
    
    def directoryExists(self, directory):
        return os.path.isdir(directory)
    
#    def directoryExistsInDatabase(self, directory):
#        return None