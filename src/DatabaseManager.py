import MySQLdb
from Logger import Logger
from PropertiesManager import PropertiesManager

class DatabaseManager():
    db = None
    
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.logger = Logger()
    
    def execute(self, sql, vars):
        if not self.isConnected():
            self.connect(True)
            
        cursor = self.db.cursor()
        cursor.execute(sql, vars)
        self.db.commit()
        
        if "insert" == sql.split(" ")[0]:
            return cursor.lastrowid
        return cursor.fetchall()
    
    def connect(self, local_call=False):
        if not local_call:
            self.logger.warn("DatabaseManager.connected() may be called by outside object.")
        self.logger.debug("attempting to open database connection...")
        self.db = MySQLdb.connect(host=self.host, 
                                  user=self.username, 
                                  passwd=self.password, 
                                  db=self.database)  
        
        self.logger.debug("database connection success: %s" % str(self.db.open == True))
          

    def isConnected(self):
        if self.db == None:
            return False
        return self.db.open == 1
    
    def close(self):
        if self.isConnected():
            self.db.close()
        