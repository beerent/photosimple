from DirectoryManager import DirectoryManager
from IntegrityManager import IntegrityManager
from DirectoryType import DirectoryType
from Logger import Logger

import os

class SyncManager(object):

    def __init__(self, database_manager):
        self.logger = Logger()
        self.directory_manager = DirectoryManager(database_manager)
        self.integrity_manager = IntegrityManager(database_manager)
    
    def syncDestinations(self):
        # get root directory
        self.logger.log("getting root directory")
        root_dir = self.directory_manager.getRootDirectory()
        
        # validate root directory's integrity
        self.logger.log("validating health on root directory '%s'" % root_dir.getDirectoryPath())
        healthy = self.integrity_manager.destinationIsHealthy(root_dir)
        self.logger.log("root directory is healthy: %s" % str(healthy))
        
        # if destination is healthy, rsync w/ every other directory
        destinations = self.directory_manager.getDirectories(DirectoryType("DESTINATION"))
        for destination in destinations:
            if not destination.isRoot():
                self.rsyncDestinations(root_dir.getDirectoryPath(), destination.getDirectoryPath())
                
    def rsyncDestinations(self, src_path, destination_path):
        self.logger.log("rsyncing '%s' to '%s'" % (src_path, destination_path))
        os.system("rsync -a %s/* %s" % (src_path, destination_path))