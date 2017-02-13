from RequestManager import RequestManager
import sys

request_manager = RequestManager()
response = request_manager.processRequest(sys.argv[1:])

#request_results = validateArguments()
#if request_results is not None:
##    logger.error(request_results)
#    exit(1)

#database_manager = getDatabaseManager()
#logger.debug("database connected pre request: %s" % str(database_manager.isConnected()))
#handleRequest(database_manager)
#logger.debug("database connected post request: %s" % str(database_manager.isConnected()))

#database_manager.close()