from SyncDestinationResult import SyncDestinationResult
from DirectoryManager import DirectoryManager
from IntegrityManager import IntegrityManager
from DirectoryType import DirectoryType
from SyncResult import SyncResult
from Logger import Logger
from Error import Error

import os

class SyncManager(object):

    def __init__(self, database_manager):
        self.logger = Logger()
        self.directory_manager = DirectoryManager(database_manager)
        self.integrity_manager = IntegrityManager(database_manager)
        
    def syncDestinationsRequest(self, name, directory):
        successful = False
        error = None
        
        synced_destinations = self.syncDestinations(name, directory)

        is_string = isinstance(synced_destinations, str)
        if is_string:
            request = "sync"
            error = Error(request, synced_destinations)
            synced_destinations = None
        else:
            successful = True
        
        sync_result = SyncResult(synced_destinations, successful, error)
        return sync_result
    
    
    
    ###
    ### Break this up into smaller functions
    ###
    def syncDestinations(self, name, directory):
        self.logger.head("STARTING DESTINATION SYNC")
        
        # get root directory
        self.logger.log("getting root directory")
        root_dir = self.directory_manager.getRootDirectory()
        self.logger.log("root directory obtained")
        
        # validate root directory's integrity
        self.logger.log("validating health on root directory '%s'" % root_dir.getPath())
        healthy = self.integrity_manager.destinationIsHealthy(root_dir).isHealthy()
        self.logger.log("root directory is healthy: %s" % str(healthy))
        if not healthy:
            err_str = "root directory is not healthy, cannot sync."
            return err_str
        
        destinations = []
        synced_destinations = []
        
        if name is not None or directory is not None:
            destination = self.directory_manager.getDirectory(DirectoryType("DESTINATION"), name, directory)
            if destination is None:
                self.logger.error("cannot sync destination %s (%s)" % (name, destination))
            destinations.append(destination)
                
        else:
            destinations = self.directory_manager.getAllDirectories(DirectoryType("DESTINATION"))

        for destination in destinations:
            sync_destination_result = None
            successful = False
            error = None
            
            if destination.isRoot():
                continue
            
            if not self.directory_manager.directoryExists(destination.getPath()):
                err_str = "cannot sync destination (unaccessible): '%s'" % destination.getName()
                error = Error("sync", err_str)
                successful = False
                
                self.logger.error(err_str)

            else:
                self.logger.log("syncing destination: '%s'" % destination.getName())
                self.rsyncDestinations(root_dir.getPath(), destination.getPath())
                self.logger.log("destination: '%s' has been successfully synced!" % destination.getName())
                successful = True
            
            sync_destination_result = SyncDestinationResult(destination, successful, error)
            synced_destinations.append(sync_destination_result)
        
        return synced_destinations
            
    def rsyncDestinations(self, src_path, destination_path):
        self.logger.log("rsyncing '%s' to '%s'" % (src_path, destination_path))
        os.system("rsync -a %s/* %s" % (src_path, destination_path))