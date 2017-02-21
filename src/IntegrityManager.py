from HealthCheckDestinationResult import HealthCheckDestinationResult
from HealthCheckResult import HealthCheckResult
from DirectoryManager import DirectoryManager
from DirectoryType import DirectoryType
from PhotoManager import PhotoManager
from FileManager import FileManager
from Logger import Logger
from Error import Error

class IntegrityManager(object):

    def __init__(self, database_manager):
        self.directory_manager = DirectoryManager(database_manager)
        self.photo_manager = PhotoManager(database_manager)
        self.file_manager = FileManager()
        self.logger = Logger()
        
    def healthCheckerRequest(self, directory, name):
        successful = False
        results = self.healthChecker(directory, name)
        error = None

        is_string = isinstance(results, (str, unicode))
        if is_string:
            request = "health check"
            error = Error(request, result)
            results = None
        else:
            successful = True
        
        health_check_result = HealthCheckResult(results, successful, error)
        return health_check_result
        
    
    def healthChecker(self, directory, name):
        health_check_destinations = []
        directories = []
        if directory is not None or name is not None:
            directory = self.directory_manager.getDirectory(DirectoryType("DESTINATION"), name, directory)
            directories.append(directory)
        else:
            directories = self.directory_manager.getAllDirectories(DirectoryType("DESTINATION"))
        
        for directory in directories:
                        
            if not self.directory_manager.directoryExists(directory.getPath()):
                err_str = "cannot check health of destination [name: '%s' | path: '%s'], directory is inaccessible." % (directory.getName(), directory.getPath())
                healthy = False
                missing_photos = []
                extra_photos   = []
                successful = False
                error = Error("health check", err_str)
                result = HealthCheckDestinationResult(directory, healthy, missing_photos, extra_photos, successful, error)
                self.logger.error(err_str)
                
            else:
                result = self.destinationIsHealthy(directory)
                                                
            health_check_destinations.append(result)

        return health_check_destinations
            
    def destinationIsHealthy(self, destination):
        log_str = "checking health of destination [name: '%s' | directory: '%s']" % (destination.getName(), destination.getPath())
        self.logger.debug(log_str)
        
        healthy = False
        missing_photos = []
        extra_photos   = []
        successful = False
        error = None
        
        #self.logger.debug("fetching sub directories")
        sub_dirs = self.directory_manager.getSubDirectories()
        
        for sub_dir in sub_dirs:
            self.logger.debug("validating health of sub directory '%s'" % sub_dir)
            full_path = destination.getPath() + sub_dir
            self.logger.debug("full path of sub directory: '%s'" % full_path)
            
            if not self.directory_manager.directoryExists(full_path):
                err_str = "directory '%s' is not accessible" % sub_dir
                error = Error('health check', err_str)
                self.logger.error(err_str)
                return HealthCheckDestinationResult(directory, healthy, missing_photos, extra_photos, successful, error)
            
            database_files = self.photo_manager.getPhotosInSubDirectory(sub_dir)
            filesystem_files = self.file_manager.getFiles(full_path)
            
            missing_sub_photos = self.getMissingPhotos(database_files, filesystem_files)
            extra_sub_photos   = self.getExtraPhotos(database_files, filesystem_files)
            missing_photos = missing_photos + missing_sub_photos
            extra_photos   = extra_photos + extra_sub_photos
        healthy = len(missing_photos) == 0 and len(extra_photos) == 0
        successful = True
            
        return HealthCheckDestinationResult(destination, healthy, missing_photos, extra_photos, successful, error)
    
    
    
    def getMissingPhotos(self, database_files, filesystem_files):
        missing_photos = []
        
        filesystem_hashes = []
        for filesystem_file in filesystem_files:
            filesystem_hashes.append(filesystem_file.getHash())

        for database_file in database_files:
            if database_file.getHash() not in filesystem_hashes:
                missing_photos.append(database_file)
                
        return missing_photos
    
    def getExtraPhotos(self, database_files, filesystem_files):
        extra_photos = []
        
        database_hashes = []
        for database_file in database_files:
            database_hashes.append(database_file.getHash())
            
        for filesystem_file in filesystem_files:
            if filesystem_file.getHash() not in database_hashes:
                extra_photos.append(filesystem_file)
                
        return extra_photos
    
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