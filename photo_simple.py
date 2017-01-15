from DirectoryManager import DirectoryManager
from PropertiesManager import PropertiesManager
from DatabaseManager import DatabaseManager
from Logger import Logger
import sys



###############################
# Request Fields
###############################

no_arg_parameters = [
                    "-v",
                    "--verbose",
                    "-h",
                    "--help"
                    ]

arg_parameters = [
                 "-r",
                 "--request",
                 "-d",
                 "--directory"
                 ]


valid_requests = [
                  "add_destination",
                  "remove_destination"
                  ]

#request fields
request = None
directory = None
verbose = None

#create logger option
logger = Logger()














###############################
# HELP MENU
###############################  
  
def helpMenu():
    ret_str =    "--verbose   (-v) verbose mode"
    ret_str += "\n--request   (-r) <request>"
    ret_str += "\n--directory (-d) <directory>"
    return ret_str





###############################
# VALIDATE ARGUMENTS
############################### 

def validateArguments():
    global valid_requests, no_arg_parameters, arg_parameters
    global request, directory
    
    if request == None:
        return "missing request (-r, --request)"
    
    if request not in valid_requests:
        ret_str = "'%s' is an invalid request" % request
        return ret_str
    
    if (request == "add_destination" or request == "remove_destination") and directory == None:
        return "missing directory (-d, --directory)"
    
    return None





############################
# PARSE REQUEST
############################

def parseRequest():
    if len(sys.argv) == 1:
        logger.error("missing arguments. (-h for help)")
        exit(1)

    arguments = sys.argv

    global request, directory, verbose
    
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

        #error in code if we get here
        else:
            log_str = "code error - not accounting for request '%s'" % arg1
            logger.error(log_str)
            exit(1)



############################
# HANDLE REQUEST
############################
     
def handleRequest(database_manager):
    global request, directory
    
    directory_manager = DirectoryManager(database_manager)

    if request == "add_destination":
        directory_manager.addDestination(directory)
    elif request == "remove_destination":
        directory_manager.removeDestination(directory)
    else:
        logger.error("request type '%s' not found in handleRequest()")
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
# MAIN REQUEST

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
