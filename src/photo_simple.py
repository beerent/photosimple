from DirectoryManager import DirectoryManager
from PropertiesManager import PropertiesManager
from DatabaseManager import DatabaseManager
from DirectoryType import DirectoryType
from BackupManager import BackupManager
from SyncManager import SyncManager
from ModeType import ModeType
from Logger import Logger
import sys



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
                 "-m", "--mode"
                 ]


valid_requests = [
                  "add_destination",
                  "remove_destination",
                  "add_source",
                  "remove_source",
                  "backup",
                  "sync"
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

#create logger option
logger = Logger()














###############################
# HELP MENU
###############################  
  
def helpMenu():

    ret_str = "--directory (-d) <directory>"
    ret_str += "\n\n--name (-n) <directory>"   
    ret_str += "\n\n--request (-r)\t\tthe type of request desired. available options listed below."
    ret_str += "\n\n   add_destination\tadd a new destination to backup photos to."
    ret_str += "\n\n   add_source\t\tadd a new directory to backup photos from."
    ret_str += "\n\n   backup\t\tinitiate a backup request."
    ret_str += "\n\n   remove_destination\tremove a backup location from photosimple. this does not delete the directory\n"
    ret_str += "\t\t\tfrom the file system, but you will no longer backup photos to this directory"
    ret_str += "\n\n   remove_source"
    ret_str += "\n\n--verbose (-v)\t\tverbose mode"
    return ret_str





###############################
# VALIDATE ARGUMENTS
############################### 

def validateArguments():
    global valid_requests, no_arg_parameters, arg_parameters
    global request, directory, name, mode
    
    #request flag is missing
    if request == None:
        return "missing request (-r, --request)"
    
    #request flag is not valid
    if request not in valid_requests:
        ret_str = "'%s' is an invalid request" % request
        return ret_str
    
    
    if request in("add_destination", "add_source") and directory == None:
        return "missing directory (-d, --directory)"
    
    if request in ("remove_destination", "remove_source") and directory == None and name == None:
        return "missing directory or name (-d, --directory, -n, --name)"
    
    if (request in ("add_destination", "add_source") and name == None):
        logger.warn("no name for destination '%s' provided" % directory)
    
    if request == "backup" and mode is None:
        logger.error("missing mode type (-m, --mode)")
        exit(1)
        
    if request == "backup":
        if mode not in valid_modes:
            return "invalid backup mode: %s" % mode
        
    
    return None




############################
# PARSE REQUEST
############################

def parseRequest():
    if len(sys.argv) == 1:
        logger.error("missing arguments. (-h for help)")
        exit(1)

    arguments = sys.argv
    verbose = False

    global request, directory, name, tag, mode
    
    i = 1
    while i < len(arguments):
        #grab current argument
        arg1 = arguments[i]
        
        # no argument parameters
        
        #verbose argument
        if (verbose == None and arg1 == "--verbose" or arg1 == "-v"):
            logger.setVerbose(True)
            verbose = True
            i = i + 1
            continue
        
        #help argument
        if arg1 == "-h" or arg1 == "--help":
            print helpMenu()
            exit(0)
        
        #verify state of request parsing
        if i + 1 == len(arguments):
            if arg1 in arg_parameters:
                err_str = "missing argument for request '%s'." % arg1
            elif arg1 in no_arg_parameters:
                err_str = "code doesn't account for parameter '%s'" % arg1
            else:
                err_str = "invalid argument '%s'." % arg1

            logger.error(err_str)
            exit(1)
            
        #continue to collect parameter
        i = i + 1

        # argument parameters
        
        #request argument
        if (arg1 == "--request" or arg1 == "-r") and request == None:
            arg2 = arguments[i]
            i = i + 1
            request = arg2
            continue

        #directory argument
        elif (arg1 == "--directory" or arg1 == "-d") and directory == None:
            arg2 = arguments[i]
            i = i + 1
            directory = arg2
            continue

        #name argument
        elif (arg1 == "--name" or arg1 == "-n") and name == None:
            arg2 = arguments[i]
            i = i + 1
            name = arg2
            continue

        #name argument
        elif (arg1 == "--mode" or arg1 == "-m") and mode == None:
            arg2 = arguments[i]
            i = i + 1
            mode = arg2
            continue
        
        #tag argument
        elif (arg1 == "--tag" or arg1 == "-t") and tag == None:
            arg2 = arguments[i]
            i = i + 1
            tag = arg2
            continue

        #error in code if we get here
        else:
            log_str = "code error - not accounting for request '%s'" % arg1
            logger.error(log_str)
            exit(1)



############################
# HANDLE REQUEST
############################
     
def handleRequest(database_manager):
    global request, directory, name, mode
    
    directory_manager = DirectoryManager(database_manager)
    backup_manager = BackupManager(database_manager)
    sync_manager = SyncManager(database_manager)
    
    if request == "add_destination":
        logger.log("running 'add destination': %s: %s" % (directory, name))
        directory_manager.addDirectory(DirectoryType("DESTINATION"), name, directory)
    elif request == "remove_destination":
        logger.log("running 'remove destination': %s: %s" % (directory, name))
        directory_manager.removeDirectory(DirectoryType("DESTINATION"), name, directory)
    
    elif request == "add_source":
        directory_manager.addDirectory(DirectoryType("SOURCE"), name, directory)
        logger.log("running 'add source': %s: %s" % (directory, name))
    elif request == "remove_source":
        directory_manager.removeDirectory(DirectoryType("SOURCE"), name, directory)
        logger.log("running 'remove source': %s: %s" % (directory, name))

    elif request == "backup":
        logger.log("running 'backup'")
        if mode is not None:
            mode = ModeType(mode)
        backup_manager.backupPhotos(mode)
        sync_manager.syncDestinations()
        
    elif request == "sync":
        logger.log("running 'sync'")
        sync_manager.syncDestinations()
        
    else:
        logger.error("request type '%s' not found in handleRequest()" % request)
        exit(1)

    
    
    
    
############################
# CREATE DATABASE MANAGER
############################
 
def getDatabaseManager():
    properties_manager = PropertiesManager()
    host = properties_manager.getProperty("db_host")[0]
    username = properties_manager.getProperty("db_username")[0]
    password = properties_manager.getProperty("db_password")[0]
    database = properties_manager.getProperty("db_database")[0]  
    return DatabaseManager(host, username, password, database)  





###############################################################################
# MAIN

parseRequest()

request_results = validateArguments()
if request_results is not None:
    logger.error(request_results)
    exit(1)

database_manager = getDatabaseManager()
logger.debug("database connected pre request: %s" % str(database_manager.isConnected()))
handleRequest(database_manager)
logger.debug("database connected post request: %s" % str(database_manager.isConnected()))

database_manager.close()