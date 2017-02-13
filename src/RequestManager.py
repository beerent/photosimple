from PropertiesManager import PropertiesManager
from DirectoryManager import DirectoryManager
from IntegrityManager import IntegrityManager
from DatabaseManager import DatabaseManager
from BackupManager import BackupManager
from DirectoryType import DirectoryType
from QueryManager import QueryManager
from SyncManager import SyncManager
from ModeType import ModeType
from Logger import Logger

class RequestManager():
        
    ###############################
    # Request Fields
    ###############################
    
    no_arg_parameters = [
                        "-v", "--verbose",
                        "-h", "--help"

                        ]
    
    arg_parameters = [
                     "-r", "--request",
                     "-d", "--directory",
                     "-n", "--name",
                     "-m", "--mode",
                     
                     #for queries
                     '--added_from',
                     '--added',
                     '--added_to',
                     '--modified_from',
                     '--modified',
                     '--modified_to'                
                     ]
    
    
    valid_requests = [
                      "add_destination",
                      "remove_destination",
                      "add_source",
                      "remove_source",
                      "backup",
                      "sync",
                      "health_check",
                      'cherry_pick'
                      ]
    
    valid_modes = [
                   "captured",
                   "today"               
                   ]
    
    
    
    #request fields
    request = None
    directory = None
    name = None
    mode = None
    tag = None
    
    #query fields
    added_from = None
    added = None
    added_to = None
    modified_from = None
    modified = None
    modified_to = None
    

    def __init__(self):
        self.logger = Logger()
        
########################################################################


    def processRequest(self, arguments):
        self.parseRequest(arguments)
        request_results = self.validateArguments()
        if request_results is not None:
            logger.error(request_results)
            exit(1)
        
        database_manager = self.getDatabaseManager()
        self.logger.debug("database connected pre request: %s" % str(database_manager.isConnected()))
        self.handleRequest(database_manager)
        self.logger.debug("database connected post request: %s" % str(database_manager.isConnected()))
        database_manager.close()



    ############################
    # PARSE REQUEST
    ############################
    
    def parseRequest(self, arguments):
        self.logger.debug("parsing request")
        
        if len(arguments) == 0:
            self.logger.error("missing arguments. (-h for help)")
            exit(1)
    
        verbose = False
        
        i = 0
        while i < len(arguments):
            #grab current argument
            arg1 = arguments[i]
            
            # no argument parameters
            
            #verbose argument
            if (verbose == None and arg1 == "--verbose" or arg1 == "-v"):
                self.logger.setVerbose(True)
                verbose = True
                i = i + 1
                continue
            
            #help argument
            if arg1 == "-h" or arg1 == "--help":
                print helpMenu()
                exit(0)
            
            #verify state of request parsing
            if i + 1 == len(arguments):
                if arg1 in self.arg_parameters:
                    err_str = "missing argument for request '%s'." % arg1
                elif arg1 in self.no_self.arg_parameters:
                    err_str = "code doesn't account for parameter '%s'" % arg1
                else:
                    err_str = "invalid argument '%s'." % arg1
    
                self.logger.error(err_str)
                exit(1)
                
            #continue to collect parameter
            i = i + 1
    
            # argument parameters
            
            #request argument
            if (arg1 == "--request" or arg1 == "-r") and self.request == None:
                arg2 = arguments[i]
                i = i + 1
                self.request = arg2
                continue
    
            #directory argument
            elif (arg1 == "--directory" or arg1 == "-d") and self.directory == None:
                arg2 = arguments[i]
                i = i + 1
                self.directory = arg2
                continue
    
            #name argument
            elif (arg1 == "--name" or arg1 == "-n") and self.name == None:
                arg2 = arguments[i]
                i = i + 1
                self.name = arg2
                continue
    
            #name argument
            elif (arg1 == "--mode" or arg1 == "-m") and self.mode == None:
                arg2 = arguments[i]
                i = i + 1
                self.mode = arg2
                continue
            
            #tag argument
            elif (arg1 == "--tag" or arg1 == "-t") and self.tag == None:
                arg2 = arguments[i]
                i = i + 1
                self.tag = arg2
                continue
            
            #added from argument
            elif (arg1 == "--added_from") and self.added_from == None:
                arg2 = arguments[i]
                i = i + 1
                self.added_from = arg2
                continue
            
            #added argument
            elif (arg1 == "--added") and self.added == None:
                arg2 = arguments[i]
                i = i + 1
                self.added = arg2
                continue
            
            #added to argument
            elif (arg1 == "--added_to") and self.added_to == None:
                arg2 = arguments[i]
                i = i + 1
                self.added_to = arg2
                continue
            
            #modified from argument
            elif (arg1 == "--modified_from") and self.modified_from == None:
                arg2 = arguments[i]
                i = i + 1
                self.modified_from = arg2
                continue
            
            #modified argument
            elif (arg1 == "--modified") and self.modified == None:
                arg2 = arguments[i]
                i = i + 1
                self.modified = arg2
                continue
            
            #modified to argument
            elif (arg1 == "--modified_to") and self.modified_to == None:
                arg2 = arguments[i]
                i = i + 1
                self.modified_to = arg2
                continue
    
            #error in code if we get here
            else:
                log_str = "code error - not accounting for request '%s'" % arg1
                self.logger.error(log_str)
                exit(1)
                
        self.logOptions()
       
       
       
       
       
       
        
        
    ###############################
    # LOG OPTIONS
    ###############################  
    
    def logOptions(self):
        self.logger.debug("request:       '%s'" % self.request)
        self.logger.debug("directory:     '%s'" % self.directory)
        self.logger.debug("name:          '%s'" % self.name)
        self.logger.debug("mode:          '%s'" % self.mode)
        self.logger.debug("added from:    '%s'" % self.added_from)
        self.logger.debug("added:         '%s'" % self.added)
        self.logger.debug("added to:      '%s'" % self.added_to)
        self.logger.debug("modified from: '%s'" % self.modified_from)
        self.logger.debug("modified:      '%s'" % self.modified)
        self.logger.debug("modified to:   '%s'" % self.modified_to)
        
   
   
   
   
        
    ###############################
    # HELP MENU
    ###############################  
      
    def helpMenu(self): 
        ret_str = "--directory (-d) <directory>"
        ret_str += "\n\n--name (-n) <directory>"   
        ret_str += "\n\n--request (-r)\t\toptions\t\tthe type of request desired. available options listed below."
        ret_str += "\n\n   add_destination\t<-d> [-n]\tadd a new destination to backup photos to."
        ret_str += "\n\n   add_source\t\t<-d> [-n]\tadd a new directory to backup photos from."
        ret_str += "\n\n   backup\t\t<> []\t\tinitiate a backup request."
        ret_str += "\n\n   heath_check\t\t<> [-d, -n]\tcheck the heath of one or all destinations."
        ret_str += "\n\n   remove_destination\t<> [-d, -n]\tremove a backup location from photosimple. this does not delete the directory\n"
        ret_str += "\t\t\t\t\tfrom the file system, but you will no longer backup photos to this directory"
        ret_str += "\n\n   remove_source\t<> [-d, -n]\tremove a source location from photosimple. photosimple will not backup from this\n"
        ret_str += "\t\t\t\t\tfrom this location anymore."
        ret_str += "\n\n   sync\t\t\t<> []\t\tinitate a synchronization between all destinations."
        ret_str += "\n\n--verbose (-v)\t\tverbose mode"
        return ret_str
    
    
    
    
    
    ###############################
    # VALIDATE ARGUMENTS
    ############################### 
    
    def validateArguments(self):     
        #request flag is missing
        if self.request == None:
            return "missing request (-r, --request)"
        
        #request flag is not valid
        if self.request not in self.valid_requests:
            ret_str = "'%s' is an invalid request" % self.request
            return ret_str
        
        
        if self.request in("add_destination", "add_source") and self.directory == None:
            return "missing directory (-d, --directory)"
        
        if self.request in ("remove_destination", "remove_source") and self.directory == None and self.name == None:
            return "missing directory or name (-d, --directory, -n, --name)"
        
        if (self.request in ("add_destination", "add_source") and self.name == None):
            self.logger.warn("no name for destination '%s' provided" % self.directory)
        
        if self.request == "backup" and self.mode is None:
            self.logger.error("missing mode type (-m, --mode)")
            exit(1)
            
        if self.request == "backup":
            if self.mode not in self.valid_modes:
                return "invalid backup mode: %s" % self.mode
        
        if self.request == 'cherry_pick':
            if self.added_from == None and \
               self.added == None \
               and self.added_to == None \
               and self.modified_from == None \
               and self.modified == None \
               and self.modified_to == None:
                return 'invalid cherry_pick: at least one query condition required.'
            
        
        return None
    
    
    ############################
    # HANDLE REQUEST
    ############################
         
    def handleRequest(self, database_manager):       
        directory_manager = DirectoryManager(database_manager)
        integrity_manager = IntegrityManager(database_manager)
        backup_manager = BackupManager(database_manager)
        query_manager = QueryManager(database_manager)
        sync_manager = SyncManager(database_manager)
        
        
        
        if self.request == "add_destination":
            self.logger.log("running 'add destination': %s: %s" % (self.directory, self.name))
            directory_manager.addDirectory(DirectoryType("DESTINATION"), self.name, self.directory)
        
        elif self.request == "remove_destination":
            self.logger.log("running 'remove destination': %s: %s" % (self.directory, self.name))
            directory_manager.removeDirectory(DirectoryType("DESTINATION"), self.name, self.directory)
        
        elif self.request == "add_source":
            directory_manager.addDirectory(DirectoryType("SOURCE"), self.name, self.directory)
            self.logger.log("running 'add source': %s: %s" % (self.directory, self.name))
        
        elif self.request == "remove_source":
            directory_manager.removeDirectory(DirectoryType("SOURCE"), self.name, self.directory)
            self.logger.log("running 'remove source': %s: %s" % (self.directory, self.name))
    
        elif self.request == "backup":
            self.logger.log("running 'backup'")
            if self.mode is not None:
                self.mode = ModeType(self.mode)
            backup_manager.startPhotoBackup(self.mode)
            sync_manager.syncDestinations()
            
        elif self.request == "sync":
            self.logger.log("running 'sync'")
            sync_manager.syncDestinations()
        
        elif self.request == "health_check":
            self.logger.log("running 'health check'")
            integrity_manager.runHealthChecker(self.directory, self.name)
        
        elif self.request == 'cherry_pick':
            self.logger.log("running 'cherry pick'")
            query_manager.queryPhotos(self.added_from, self.added, self.added_to, \
                                      self.modified_from, self.modified, self.modified_to)
            
            
            
            
        else:
            self.logger.error("request type '%s' not found in handleRequest()" % self.request)
            exit(1)
    
        
        
        
        
    ############################
    # CREATE DATABASE MANAGER
    ############################
     
    def getDatabaseManager(self):
        properties_manager = PropertiesManager()
        host = properties_manager.getProperty("db_host")[0]
        username = properties_manager.getProperty("db_username")[0]
        password = properties_manager.getProperty("db_password")[0]
        database = properties_manager.getProperty("db_database")[0]  
        return DatabaseManager(host, username, password, database)  
    
    
    
    
