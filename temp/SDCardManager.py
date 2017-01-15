from PropertiesManager import PropertiesManager
import commands
import threading
import time
from SDCard import SDCard 
from DirectoryManager import DirectoryManager
from MD5Manager import MD5Manager
from Photo import Photo


class SDCardManager(object):

    def __init__(self):
        self.sd_connected_array = None
        self.sd_scanner_running = False
        
    def getConnectedSDCards(self, database_manager):
        sql = "select sd_card_id, sd_name, sd_path from sd_cards"
        results = database_manager.execute(sql)
        
        sd_cards = []
        for row in results:
            sd_card_id = row[0]
            sd_name = row[1]
            sd_path = row[2]
            
            sd_card_obj = SDCard(sd_card_id, sd_name, sd_path)
            sd_cards.append(sd_card_obj)
        
        return sd_cards
        
    def getPhotosOnSDCard(self, sd_card):
        directory_manager = DirectoryManager()
        md5_manager = MD5Manager()
        results = directory_manager.getFilesInDirectory(sd_card.getPath())
        
        
        photos = []
        for photo_name in results:
            photo_path = sd_card.getPath() + "/" + photo_name
            photo_md5 = md5_manager.generateMD5OfFile(photo_path)
            photos.append(Photo(None, photo_path, photo_md5))
        return photos
            
        

    def getConnectionStatus(self, sd_path):
        if self.sd_connected_array == None:
            self.updateSDConnectionStatus()
        return self.sd_connected_array[sd_path]
    
    def updateSDConnectionStatus(self):
        properties_manager = PropertiesManager()
        properties_manager.loadProperties()
        sd_card_names = properties_manager.getProperty("sd_paths")
        sd_connected_array = {}
        
        for sd_card in sd_card_names:
            sd_connected_array[sd_card] = "true" in commands.getstatusoutput("if test -d "+ sd_card +"; then echo \"true\"; fi" )
        self.sd_connected_array = sd_connected_array



    #####################
    #      THREAD        
    #####################
    def startSDCardThread(self):
        self.t = threading.Thread(target=self.startSDCardScanner)
        self.t.start()
        
    def stopSDCardScanner(self):
        self.sd_scanner_running = False
    
    def startSDCardScanner(self):
        self.sd_scanner_running = True
        while self.sd_scanner_running:
            self.updateSDConnectionStatus()
            time.sleep(2)