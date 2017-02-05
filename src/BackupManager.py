from DirectoryManager import DirectoryManager
from PhotoManager import PhotoManager
from DateManager import DateManager
from FileManager import FileManager
from PhotoDAO import PhotoDAO
from Logger import Logger

class BackupManager(object):
    
    def __init__(self, database_manager):
        self.directory_manager = DirectoryManager(database_manager)
        self.photo_manager = PhotoManager(database_manager)
        self.photo_dao = PhotoDAO(database_manager)
        self.date_manager = DateManager()
        self.file_manager = FileManager()
        self.logger = Logger()
        
        
      
    def startPhotoBackup(self, mode):
        present_source_directories = self.directory_manager.getPresentDirectories()
        if len(present_source_directories) == 0:
            self.logger.error("no source directory found, cannot continue with backup.")
            exit(1)    
        present_root_destination = self.directory_manager.getRootDirectory()       
        if present_root_destination == None:
            self.logger.error("root destination not found, cannot continue with backup.")
            exit(1)        
        database_file_hashes = self.photo_manager.getPhotoHashes()
        self.backupPhotos(present_source_directories, present_root_destination, database_file_hashes, mode)



    def backupPhotos(self, present_source_directories, present_root_destination, database_file_hashes, mode):
        total_processed = 0
        total_backed_up = 0
        for source in present_source_directories:
            files = self.file_manager.getFiles(source.getDirectoryPath())
            for file in files:
                total_processed = total_processed + 1
                if file.getHash() in database_file_hashes:
                    self.logger.debug("skipping '%s', already in database" % file.getPath())
                    continue
                self.backupPhoto(file, source, present_root_destination, mode)
                database_file_hashes.append(file.getHash())
                total_backed_up = total_backed_up + 1
        self.logger.log("backup complete.")  
        self.logger.log("%s files processed" % total_processed)
        self.logger.log("%s files backed up" % total_backed_up)
        self.logger.log("%s files already backed up" % (total_processed - total_backed_up))
        
        
    #Backs up a single photo to a desired destination
    def backupPhoto(self, file, source, destination, mode):
        if mode.getModeType() == "TODAY":
            sub_dir = self.directory_manager.createTodaysDirectory(file, destination)
        elif mode.getModeType() == "CAPTURED":
            sub_dir = self.directory_manager.createModifiedDirectory(file, destination)
        else:
            self.logger.error("invalid mode type found: '%s'" % mode.getModeType())
            exit(1)
            
        full_dir = destination.getDirectoryPath() + sub_dir
        self.file_manager.backupFile(file.getPath(), full_dir)
        self.photo_dao.backupPhoto(file.getName(), sub_dir, file.getHash(), file.getModified(), source, destination)