from datetime import datetime

class Logger(object):
    instance = None
    verbose = False
    
    def __new__(self):
        if not self.instance:
            self.instance = super(Logger, self).__new__(self)
        return self.instance
    
    def setVerbose(self, verbose):
        self.verbose = verbose
        if verbose:
            self.debug("verbose: ON")

    def isVerbose(self):
        return self.verbose
    
    def debug(self, log):
        if self.isVerbose():
            string = "%s [debug] %s" % (self.getDateTime(), log)
            self.executeLog(string)
    
    def log(self, log):
        string = "%s [log]   %s" % (self.getDateTime(), log)
        #if self.isVerbose():
        self.executeLog(string)
    
    def warn(self, log):
        string = "%s [warn]  %s" % (self.getDateTime(), log)
        #if self.isVerbose():
        self.executeLog(string)
    
    def error(self, log):
        string = "%s [error] %s" % (self.getDateTime(), log)
        #if self.isVerbose():
        self.executeLog(string)
        
    def executeLog(self, string):
        print string
        with open("photosimple.log", "a") as log_file:
            log_file.write("%s\n" % string)
    
    def getDateTime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")