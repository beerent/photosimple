from datetime import datetime
from PropertiesManager import PropertiesManager
import os

class Logger(object):
    instance = None
    verbose = False
    log_directory = None
    
    def __new__(self):
        if not self.instance:
            self.instance = super(Logger, self).__new__(self)
            properties_manager = PropertiesManager()
            self.log_directory = properties_manager.getProperty("log_directory")[0]
            if not os.path.isdir(self.log_directory):
                raise Exception("log directory '%s' doesn't exist. fatal error." % self.log_directory)
            
        return self.instance
    
    def setVerbose(self, verbose):
        self.verbose = verbose
        if verbose:
            self.debug("verbose: ON")

    def isVerbose(self):
        return self.verbose
    
    def head(self, msg):
        self.log("")
        self.log("")
        self.log("################################################################")
        self.log("# %s" % msg)
        self.log("################################################################")
        self.log("")
        self.log("")
        
    def debug(self, log):
        string = "%s [debug] %s" % (self.getDateTime(), log)
        if self.isVerbose():
            self.printLog(string)
        self.storeLog(string)
    
    def log(self, log):
        string = "%s [log]   %s" % (self.getDateTime(), log)
        #if self.isVerbose():
        self.printLog(string)
        self.storeLog(string)
    
    def warn(self, log):
        string = "%s [warn]  %s" % (self.getDateTime(), log)
        #if self.isVerbose():
        self.printLog(string)
        self.storeLog(string)
    
    def error(self, log):
        string = "%s [error] %s" % (self.getDateTime(), log)
        #if self.isVerbose():
        self.printLog(string)
        self.storeLog(string)
        
    def printLog(self, string):
        print(string)
        
    def storeLog(self, string):
        log_directory = self.log_directory + "/photosimple.log"
        with open(log_directory, "a") as log_file:
            log_file.write("%s\n" % string)
    
    def getDateTime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")