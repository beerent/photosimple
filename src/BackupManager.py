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
        
        
      
    def photoBackupRequest(self, mode):
        
        backup_source_directories = None
        successful = False
        error = None
        
        ###
        ### change to get all directories and create an error if a source cannot be accessed
        ### or not. debate if this is an "error". consider I just want to backup my one SD card, not all
        ###
        present_source_directories = self.directory_manager.getAllDirectories(DirectoryType("SOURCE"))
        if len(present_source_directories) == 0:
            err_str = "no source directory found, cannot continue with backup."
            self.logger.error(err_str)
            return err_str
            
        present_root_destination = self.directory_manager.getRootDirectory()       
        if present_root_destination == None:
            err_str = "root destination not found, cannot continue with backup."
            self.logger.error(err_str)
            return err_str
        
        database_file_hashes = self.photo_manager.getPhotoHashes()
        result = self.backupPhotos(present_source_directories, present_root_destination, database_file_hashes, mode)
        
        is_string = isinstance(result, (str, unicode))
        if is_string:
            request = "backup"
            error = Error(request, result)
            return BackupResult(None, successful, error)
        
        successful = True
        return BackupResult(result, successful, None)

    def backupPhotos(self, present_source_directories, present_root_destination, database_file_hashes, mode):
        self.logger.head("STARTING SOURCE BACKUP")
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
                        is_string = isinstance(backup_photo_result, (str, unicode))
                        if is_string:
                            error = Error("backup", backup_photo_result)
                            break
                                            
                        database_file_hashes.append(file.getHash())
                        backed_up = total_backed_up + 1

                successful = True
                        
            backup_source_directory_result = BackupSourceResult(source, processed, backed_up, successful, error)
            backup_source_directories.append(backup_source_directory_result)
        self.logger.log("backup complete.")
        return backup_source_directories
        
    #Backs up a single photo to a desired destination
    def backupPhoto(self, file, source, destination, mode):
        if mode.getModeType() == "TODAY":
            sub_dir = self.directory_manager.createTodaysDirectory(file, destination)
        elif mode.getModeType() == "CAPTURED":
            sub_dir = self.directory_manager.createModifiedDirectory(file, destination)
        else:
            err_msg = "invalid mode type found: '%s'" % mode.getModeType()
            self.logger.error(err_msg)
            return err_msg
            
            
        full_dir = destination.getDirectoryPath() + sub_dir
        new_file_name = file.getHash() + ".jpg"
        self.file_manager.copyFile(file.getPath(), full_dir + new_file_name)
        self.photo_dao.backupPhoto(new_file_name, sub_dir, file.getHash(), file.getModified(), source, destination)
        return True