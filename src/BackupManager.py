from DirectoryManager import DirectoryManager
from DirectoryType import DirectoryType
from FileManager import FileManager
from Logger import Logger

class BackupManager(object):
    
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.directory_manager = DirectoryManager(database_manager)
        self.file_manager = FileManager()
        self.logger = Logger()
            
    def backupPhotos(self):
        #for every source, backup to every destination
        source_directories = self.directory_manager.getDirectories(DirectoryType("SOURCE"))
        destination_directories = self.directory_manager.getDirectories(DirectoryType("DESTINATION"))
        
        present_source_directories = []
        present_destination_directories = []
        
        for source_directory in source_directories:
            source_path = source_directory.getDirectoryPath()
            if not self.directory_manager.directoryExists(source_path):
                self.logger.debug("source '%s' does not exist or is not accessible" % source_directory.getDirectoryName())
                continue
            self.logger.debug("source '%s' is present and accessible." % source_directory.getDirectoryName())
            present_source_directories.append(source_path)
            
        for destination_directory in destination_directories:
            destination_path = destination_directory.getDirectoryPath()
            if not self.directory_manager.directoryExists(destination_path):
                self.logger.debug("destination '%s' does not exist or is not accessible" % destination_directory.getDirectoryName())
                continue
            self.logger.debug("destination '%s' is present and accessible." % destination_directory.getDirectoryName())
            present_destination_directories.append(source_path)
        
        for source in present_source_directories:
            files = self.file_manager.getFiles(source)
        
        return None