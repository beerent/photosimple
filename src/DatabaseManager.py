from PropertiesManager import PropertiesManager
from warnings import filterwarnings
from Logger import Logger
import MySQLdb


class DatabaseManager():
    db = None
    
    def __init__(self, host, username, password, database):
        #warnings are for the weak, so ignore them!
        filterwarnings('ignore', category = MySQLdb.Warning)
        
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.logger = Logger()
    
    #accepts:
    #  - SQL string
    #  - tuple of variables for the SQL string
    #
    #returns:
    #  - insert id if insert
    #  - query results if query
    #
    #logic:
    #  - connect to database if not connected
    #  - execute SQL query
    def execute(self, sql, vars):
        #one connection per request
        if not self.isConnected():
            self.connect(True)
            
        cursor = self.db.cursor()
        cursor.execute(sql, vars)
        self.db.commit()
        
        #if this is an insert request, return the inserted ID
        if "insert" == sql.split(" ")[0]:
            return cursor.lastrowid

        #returns all queried content
        return cursor.fetchall()
    
    
    #accepts: optional boolean variable
    #
    #establishes a new connection with the database
    def connect(self, local_call=False):
        self.logger.debug("connecting to database...")
        if not local_call:
            self.logger.warn("DatabaseManager.connected() may be called by outside object.")
        self.logger.debug("attempting to open database connection...")
        self.db = MySQLdb.connect(host=self.host, 
                                  user=self.username, 
                                  passwd=self.password, 
                                  db=self.database)  
        
        self.logger.debug("database connection success: %s" % str(self.db.open == True))
          
    #returns true if connection to database is live
    def isConnected(self):
        if self.db == None:
            return False
        return self.db.open == 1
    
    #kills connection to database
    def close(self):
        if self.isConnected():
            self.db.close()
        