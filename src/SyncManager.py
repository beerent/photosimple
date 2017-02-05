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
        self.logger.head("STARTING DESTINATION SYNC")
        
        # get root directory
        self.logger.log("getting root directory")
        root_dir = self.directory_manager.getRootDirectory()
        self.logger.log("root directory obtained")
        
        # validate root directory's integrity
        self.logger.log("validating health on root directory '%s'" % root_dir.getDirectoryPath())
        healthy = self.integrity_manager.destinationIsHealthy(root_dir)
        self.logger.log("root directory is healthy: %s" % str(healthy))
        if not healthy:
            exit(1)
        
        # if destination is healthy, rsync w/ every other directory
        destinations = self.directory_manager.getDirectories(DirectoryType("DESTINATION"))
        for destination in destinations:
            if not destination.isRoot():
                if not self.directory_manager.directoryExists(destination.getDirectoryPath()):
                    self.logger.log("cannot sync destination: '%s'" % destination.getDirectoryName())
                    continue
                else:
                    self.logger.log("syncing destination: '%s'" % destination.getDirectoryName())
                    self.rsyncDestinations(root_dir.getDirectoryPath(), destination.getDirectoryPath())
                    self.logger.log("destination: '%s' has been successfully synced!" % destination.getDirectoryName())
                
    def rsyncDestinations(self, src_path, destination_path):
        self.logger.log("rsyncing '%s' to '%s'" % (src_path, destination_path))
        os.system("rsync -a %s/* %s" % (src_path, destination_path))