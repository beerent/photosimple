from DatabaseManager import DatabaseManager
from SDCardManager import SDCardManager
from BackupManager import BackupManager


class PhotoManager(object):

    def __init__(self):
        self.database_manager = DatabaseManager()
        self.sd_card_manager = SDCardManager()
        self.backup_manager = BackupManager()
        self.directory_manager = DirectoryManager()
        
    def imagesAreEqual(self, im1, im2):
        print "comparing %s vs %s" % (im1, im2)
        return ImageChops.difference(Image.open(im1), Image.open(im2)).getbbox() is None
    
    def backupSDCards(self, only_new):
        sd_cards = self.sd_card_manager.getConnectedSDCards(database_manager)
        backups = self.backup_manager.getBackupDirectories(database_manager) 
        
        for sd_card in sd_cards:
            sd_card_photos = self.sd_card_manager.getPhotosOnSDCard(sd_card)
            for sd_photo in sd_card_photos:               
                for backup in backups:
                    if only_new:
                        if not self.photoExists(backup, sd_photo):
                            todays_dir = directory_manager.createTodaysDirectory(backup_directory)
                            self.backupAndAddPhoto(backup, sd_photo)
                    else:
                        return None
                
    def photoExists(self, backup, photo):
        sql = "select photo_id from photos where md5 = %s" % (photo.getMD5() ,)
        results = self.database_manager.execute(sql)
        print results
        return False
          
    def backupAndAddPhoto(self, target_path, photo):      
        sql = "insert into photos (photo_id, md5, photo_path) values (%s, %s)" % (photo.getMD5(), photo.getPath())
        print sql
#        self.directory_manager.copyFile(photo.getPath(), backup.getPath() + )
#        results = self.database_manager.execute(sql)
            
        #for each SD card
            #for each Backup Directory in database
                #for each photo on SD Card
                    #if only_new:
                        #if doesnt exist; add
                        #else skip
                    #else
                        #add
                        #if others exist, map to each
                    
        
        
        
        
        
        
        
        
        
        
           
        '''backup_directories = self.properties_manager.getProperty("backup_directories")
        sd_cards = self.properties_manager.getProperty("sd_paths")
        
        for backup_directory in self.backup_directories:
            todays_directory = self.directory_manager.createTodaysDirectory(backup_directory)
            for sd_card_path in sd_cards:
                for photo in self.directory_manager.getFilesInDirectory(sd_card):
                    photo_dir = sd_card_paths + "/" + photo
                    file_exists = False
                    if only_new:
                        max_days = self.properties_manager.getProperty("backup_new_max_days")
                        
                        
        
        
        
        
        
        
        
        for backup_directory in self.backup_directories:
            #print "A"
            todays_directory = self.directory_manager.createTodaysDirectory(backup_directory)
            for sd_card in self.sd_cards:
                #print "B"
                for photo in self.directory_manager.getFilesInDirectory(sd_card):
                    #print "C"
                    photo_dir = sd_card + "/" + photo
                    file_exists = False
                    if only_new:
                        max_days = self.properties_manager.getProperty("backup_new_max_days")
                        directories = self.directory_manager.getPastNDirectoriesRecursive(backup_directory, max_days)
                        for directory in directories:
                            #print "scanning directory %s" % directory
                            existing_photos = self.directory_manager.getFilesInDirectory(directory)
                            for existing_photo in existing_photos:
                                existing_photo_dir = directory + "/" + existing_photo
                                if filecmp.cmp(existing_photo_dir.replace("\\ ", " "), photo_dir.replace("\\ ", " ")):
                                    file_exists = True
                                    break                                
                    else:
                        todays_directory_files = self.directory_manager.getFilesInDirectory(todays_directory)
                        for existing_photo in todays_directory_files:
                            existing_photo_dir = todays_directory + "/" + existing_photo
                            #print "photo: %s" % existing_photo
                            #existing_photo_md5 = hashlib.md5(open(existing_photo_dir.replace("\\ ", " "),'rb').read()).hexdigest()
                            #photo_md5 = hashlib.md5(open(photo_dir.replace("\\ ", " "), 'rb').read()).hexdigest()
                            #if existing_photo_md5 == photo_md5:
                            #if filecmp.cmp(existing_photo_dir.replace("\\ ", " "), photo_dir.replace("\\ ", " ")):
                                                
            if self.imagesAreEqual(existing_photo_dir.replace("\\ ", " "), photo_dir.replace("\\ ", " ")):
                                file_exists = True
                                break
                    
                    if not file_exists:
                        print "copying '%s' to '%s'" % (photo_dir, todays_directory)   
                    
#                        self.directory_manager.copyFile(photo_dir, todays_directory)
'''
                        
                        
    
    def backupConnectedSDCardsAll(self):
        self.backupSDCards(False)
        
    def backupConnectedSDCardsNew(self):
        self.backupSDCards(True)
#        for backup_directory in self.backup_directories:
#            directories = directory_manager.getPastNDirectoriesRecursive(backup_directory, 30)
#            print directories
#            print len(directories)
        
        #for every backup dir:
            #for every sd card:
                #for every photo on sd card:  
                    #either:
                        #backup into todays dir if doesnt exist
                        #or
                        #backup into todays dir if doesn't exist in last x amount of days (dirs)  
            
    
    
 #   def backupConnectedSDCards(self):
#        for backup_directory in backup_directories:
#            #make sure todays directory exists
#            full_backup_directory = directory_manager.createTodaysDirectory(backup_directory)            
#            existing_photos = directory_manager.getFilesInDirectory(full_backup_directory).split("\n")
#            
#            for sd_card in sd_cards:
#                connection_status = sd_card_manager.getConnectionStatus(sd_card)
#                if connection_status:
#                    photos = directory_manager.getFilesInDirectory(sd_card).split("\n")
#                    for photo in photos:
#                        photo_path = sd_card + "/" + photo
#                        photo_exists = False
#                        for existing_photo in existing_photos:
#                            existing_photo_path = full_backup_directory + "/" + existing_photo
#                            if filecmp.cmp(existing_photo_path, photo_path.replace("\\ ", " ")):
#                                photo_exists = True
#                                continue
#                        if not photo_exists:
#                            print "copying file %s" % (photo_path, )
#                            directory_manager.copyFile(photo_path, full_backup_directory)