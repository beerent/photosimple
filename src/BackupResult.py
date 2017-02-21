class BackupResult():
    
    def __init__(self, backup_source_directories, successful, error):
        self.backup_source_directories = []
        self.processed = 0
        self.backed_up = 0
        self.successful = False
        self.error = None
        
        if backup_source_directories is not None:
            for dir in backup_source_directories:
                self.addBackupSourceDirectory(dir)

        if successful is not None:
            self.successful = successful
            
        if error is not None:
            self.error = error
    
    def addBackupSourceDirectory(self, backup_source_directory):
        self.backup_source_directories.append(backup_source_directory)
        self.processed = self.processed + backup_source_directory.getProcessed()
        self.backed_up = self.backed_up + backup_source_directory.getBackedUp()
    
    def getBackupSourceDirectories(self):
        return self.backup_source_directories
    
    def setError(self, error):
        self.error = error
        
    def setProcessed(self):
        self.processed = processed
        
    def getProcessed(self):
        return self.processed
        
    def getError(self):
        return self.error