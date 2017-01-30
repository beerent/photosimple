from DirectoryManager import DirectoryManager
from DirectoryType import DirectoryType
from PhotoManager import PhotoManager
from DateManager import DateManager
from FileManager import FileManager
from PhotoDAO import PhotoDAO
from Logger import Logger

class BackupManager(object):
    
    def __init__(self, database_manager):
        self.database_manager = database_manager
        
        self.directory_manager = DirectoryManager(database_manager)
        self.photo_manager = PhotoManager(database_manager)
        self.photo_dao = PhotoDAO(database_manager)
        self.date_manager = DateManager()
        self.file_manager = FileManager()
        self.logger = Logger()
      
    def backupPhotos(self, mode):
        source_directories = self.directory_manager.getDirectories(DirectoryType("SOURCE"))
        destination_directories = self.directory_manager.getDirectories(DirectoryType("DESTINATION"))
        
        present_source_directories = []
        present_root_destination = None
        present_destination_directories = []
        
        for source_directory in source_directories:
            source_path = source_directory.getDirectoryPath()
            if not self.directory_manager.directoryExists(source_path):
                self.logger.debug("source '%s' does not exist or is not accessible" % source_directory.getDirectoryName())
                continue
            self.logger.debug("source '%s' is present and accessible." % source_directory.getDirectoryName())
            present_source_directories.append(source_directory)
            
        for destination_directory in destination_directories:
            destination_path = destination_directory.getDirectoryPath()
            if not self.directory_manager.directoryExists(destination_path):
                self.logger.debug("destination '%s' does not exist or is not accessible" % destination_directory.getDirectoryName())
                continue
            self.logger.debug("destination '%s' is present and accessible." % destination_directory.getDirectoryName())
            if destination_directory.isRoot():
                present_root_destination = destination_directory
                self.logger.debug("root destination '%s' is found" % destination_directory.getDirectoryName())
            else:
                present_destination_directories.append(destination_directory)
                
        if present_root_destination == None:
            self.logger.error("root destination not found, cannot continue with backup")
            exit(1)
        
        #for every destination, must create todays year, todays month and todays day
        #in this case, create just one for root dir, and then create them when sync is happening
        
        #NOTE: use rsync to sync the rest of the folders?
        
        #NOTE: change/audit log ?
        
        database_file_hashes = self.photo_manager.getPhotoHashes()

        total_processed = 0
        total_backed_up = 0
        for source in present_source_directories:
            files = self.file_manager.getFiles(source.getDirectoryPath())
            i = 0
            for file in files:
                i = i + 1
                if file.getHash() in database_file_hashes:
                    self.logger.debug("%s) skipping '%s', already in database" % (str(i), file.getPath()))
                    continue
                self.backupPhoto(file, source, present_root_destination, mode)
                database_file_hashes.append(file.getHash())
                total_backed_up = total_backed_up + 1
            total_processed = total_processed + i
        
        
        self.logger.log("%s files processed" % total_processed)
        self.logger.log("%s files backed up" % total_backed_up)
        self.logger.log("%s files already backed up" % (total_processed - total_backed_up))
        return None
    
    
    def backupPhoto(self, file, source, destination, mode):
        sub_dir = self.createDirectory(file, mode, destination)
        full_dir = destination.getDirectoryPath() + sub_dir
        self.file_manager.backupFile(file.getPath(), full_dir)
        self.photo_dao.backupPhoto(file.getName(), sub_dir, file.getHash(), file.getModified(), source, destination)
        
        
    def createDirectory(self, file, mode, destination):
        self.logger.debug("creating directory for file '%s' with mode type %s" % (file.getName(), mode.getModeType()))
        year = None
        month = None
        day = None
        
        if mode.getModeType() == "TODAY":
            year = self.date_manager.getYear()
            month = self.date_manager.getMonth()
            day = self.date_manager.getDay()

        elif mode.getModeType() == "CAPTURED":
            modified_date = file.getModified()
            year = self.date_manager.getCreatedYear(modified_date)
            month = self.date_manager.getCreatedMonth(modified_date)
            day = self.date_manager.getCreatedDay(modified_date)
        
        self.directory_manager.createDateDirectory(year, month, day, destination.getDirectoryPath())
        sub_dir = year + "/" + month + "/" + day + "/"
        return sub_dir