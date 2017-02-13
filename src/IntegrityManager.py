from DirectoryManager import DirectoryManager
from DirectoryType import DirectoryType
from PhotoManager import PhotoManager
from FileManager import FileManager
from Logger import Logger

class IntegrityManager(object):

    def __init__(self, database_manager):
        self.directory_manager = DirectoryManager(database_manager)
        self.photo_manager = PhotoManager(database_manager)
        self.file_manager = FileManager()
        self.logger = Logger()
    
    def runHealthChecker(self, directory, name):
        directories = []
        if directory is not None or name is not None:
            directory = self.directory_manager.getDirectory(DirectoryType("DESTINATION"), name, directory)
            directories.append(directory)
        else:
            directories = self.directory_manager.getAllDirectories(DirectoryType("DESTINATION"))
        
        for directory in directories:
            if not self.directory_manager.directoryExists(directory.getDirectoryPath()):
                log_str = "cannot check health of destination [name: '%s' | directory: '%s'], directory is inaccessible."
                self.logger.log(log_str)
                continue
            log_str = "checking health of destination [name: '%s' | directory: '%s']" % (directory.getDirectoryName(), directory.getDirectoryPath())
            self.logger.log(log_str)
            result = self.destinationIsHealthy(directory)
            self.logger.log("directory '%s' is healthy: %s" % (directory.getDirectoryName(), str(result)))
            
            
    def destinationIsHealthy(self, destination):
        self.logger.log("getting sub directories")
        sub_dirs = self.directory_manager.getSubDirectories()
        
        for sub_dir in sub_dirs:
            self.logger.log("validating health of sub directory '%s'" % sub_dir)
            full_path = destination.getDirectoryPath() + sub_dir
            self.logger.debug("full path of sub directory: '%s'" % full_path)
            
            if not self.directory_manager.directoryExists(full_path):
                self.logger.error("directory '%s' does not exist in destination, but does in database." % sub_dir)
                return False
            
            database_files = self.photo_manager.getPhotosInSubDirectory(sub_dir)
            filesystem_files = self.file_manager.getFiles(full_path)
            
            result = self.compareFiles(database_files, filesystem_files, sub_dir)
            if not result:
                return result
        return True
    
    
    

    def compareFiles(self, database_files, filesystem_files, dir):
        database_files_count = len(database_files)
        filesystem_files_count = len(filesystem_files)
        if database_files_count != filesystem_files_count:
            self.logger.error("mismatch file count between database (%s) and filesystem(%s) in sub directory: %s" % (str(database_files_count), str(filesystem_files_count), dir))
            return False
        self.logger.debug("file count matches between database and filesystem (%s) for sub directory: %s" % (str(database_files_count), dir))
        
        database_file_hashes = []
        file_system_hashes = []
        for database_photo in database_files:
            database_file_hashes.append(database_photo.getHash())
        for file_system_photo in filesystem_files:
            file_system_hashes.append(file_system_photo.getHash())
            
        for database_hash in database_file_hashes:
            if database_hash not in file_system_hashes:
                self.logger.error("photo hash '%s' found in database but not file system" % database_hash)
                return False   
        for file_system_hash in file_system_hashes:
            if file_system_hash not in database_file_hashes:
                self.logger.error("photo hash '%s' found on file system but not database" % file_system_hash)
                return False
        return True