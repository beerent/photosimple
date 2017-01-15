from Backup import Backup

class BackupManager(object):
    
    def __init__(self):
        nothing = 1
    
    def getBackupDirectories(self, database_manager):
        sql = "select backup_id, backup_path from backups"
        results = database_manager.execute(sql)
        
        directories = []
        for row in results:
            backup_id = row[0]
            backup_path = row[1]
            directories.append(Backup(backup_id, backup_path))
        
        return directories
        