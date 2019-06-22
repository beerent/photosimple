from BackupSourceResult import BackupSourceResult
from DirectoryManager import DirectoryManager
from DirectoryType import DirectoryType
from BackupResult import BackupResult
from PhotoManager import PhotoManager
from FileManager import FileManager
from Response import Response
from PhotoDAO import PhotoDAO
from Logger import Logger
from Error import Error

class BackupManager(object):
    
    def __init__(self, database_manager):
        self.directory_manager = DirectoryManager(database_manager)
        self.photo_manager = PhotoManager(database_manager)
        self.photo_dao = PhotoDAO(database_manager)
        self.file_manager = FileManager()
        self.logger = Logger()
        
        
    # accepts: ModeType "mode"
    # returns:BackupResult
    
    # Logic:
    # function initiates a backup request. 
    def photoBackupRequest(self, mode):
        backup_source_directories = None
        request = "backup"
        successful = False
        error = None
        
        # get all source directories
        # return error if none are accessible.
        present_source_directories = self.directory_manager.getAllDirectories(DirectoryType("SOURCE"))
        if len(present_source_directories) == 0:
            err_str = "no source directory found, cannot continue with backup."
            self.logger.error(err_str)
            error = Error(request, err_str)
            return BackupRequest(None, successful, error)
            
        
        # get root directory
        # return error if not accessible.
        present_root_destination = self.directory_manager.getRootDirectory()       
        if present_root_destination == None:
            err_str = "root destination not found, cannot continue with backup."
            self.logger.error(err_str)
            error = Error(request, err_str)
            return BackupRequest(None, successful, error)
        
        result = self.backupPhotos(present_source_directories, present_root_destination, mode)
        
        is_string = isinstance(result, str)
        if is_string:
            self.logger.error(result)
            error = Error(request, result)
            return BackupResult(None, successful, error)
        
        successful = True
        
        #should kick off sync here.
        
        return BackupResult(result, successful, None)

    
    #accepts: - list of present source directories
    #         - present root destination directory
    #         - mode type: specifying if we're storing by added or created date
    #
    #returns: a list of source directories that were accessed during the backup.
    #
    #logic:
    # backs up all new photos from all present source directories to a root destination.
    def backupPhotos(self, present_source_directories, present_root_destination, mode):
        self.logger.head("STARTING SOURCE BACKUP")
        
        database_file_hashes = self.photo_manager.getPhotoHashes()
        backup_source_directories = []
        
        for source in present_source_directories:
            error = None
            successful = False
            processed = 0
            backed_up = 0
            if not self.directory_manager.directoryExists(source.getPath()):
                err_str ="source is not accessible"
                error = Error("backup", err_str)
            else:
                files = self.file_manager.getFiles(source.getPath())
                for file in files:
                    processed = processed + 1
                    if file.getHash() in database_file_hashes:
                        self.logger.debug("skipping '%s', already in database" % file.getPath())
                    
                    else:
                        backup_photo_result = self.backupPhoto(file, source, present_root_destination, mode)
                        
                        #if string, an error occurred. associate error with source directory, and break loop
                        is_string = isinstance(backup_photo_result, str)
                        if is_string:
                            error = Error("backup", backup_photo_result)
                            break
                                            
                        database_file_hashes.append(file.getHash())
                        backed_up = backed_up + 1

                successful = True
                        
            backup_source_directory_result = BackupSourceResult(source, processed, backed_up, successful, error)
            backup_source_directories.append(backup_source_directory_result)
        self.logger.log("backup complete.")
        return backup_source_directories
     
    #accepts: 
    #  - a file
    #  - source directory
    #  - destination directory
    #  - mode type
    #
    #returns:
    #  - returns True if successful
    #  - returns a string error message if fails   
    #
    #logic:
    # backs up a single photo to a desired destination. 
    # also stores the successful result in database.
    def backupPhoto(self, file, source, destination, mode):
        if mode.getModeType() == "TODAY":
            sub_dir = self.directory_manager.createTodaysDirectory(file, destination)
        elif mode.getModeType() == "CAPTURED":
            sub_dir = self.directory_manager.createModifiedDirectory(file, destination)
        else:
            err_msg = "invalid mode type found: '%s'" % mode.getModeType()
            self.logger.error(err_msg)
            return err_msg
            
            
        full_dir = destination.getPath() + sub_dir
        new_file_name = file.getHash() + ".jpg"
        self.file_manager.copyFile(file.getPath(), full_dir + new_file_name)
        self.photo_dao.backupPhoto(new_file_name, sub_dir, file.getHash(), file.getModified(), source, destination)
        return True