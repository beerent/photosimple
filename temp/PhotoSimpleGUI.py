from Tkinter import *
import Tkinter
import tkMessageBox
import threading
import os
import time
from SDCardManager import SDCardManager
from DateManager import DateManager
from DirectoryManager import DirectoryManager
from PropertiesManager import PropertiesManager
from PhotoManager import PhotoManager

class PhotoSimpleGUI(object):
    
    def __init__(self):
        self.sd_card_img = None
        self.sd_scanner_running = False
        self.sd_scanner_thread = None
        
    ########################
    # THREADS
    ########################
    
    def startThreads(self):
        #start sd scanner thread
        print "starting threads"
        self.sd_scanner_thread = threading.Thread(target=self.startSDScannerThread)
        self.startSDScanner()
        self.sd_scanner_thread.start()
    
    def stopSDScanner(self):
        self.sd_scanner_running = False
        
    def startSDScanner(self):
        self.sd_scanner_running = True
        
    def startSDScannerThread(self):
        self.sd_card_manager = SDCardManager()
        
        properties_manager = PropertiesManager()
        properties_manager.loadProperties()
        sd_paths = properties_manager.getProperty("sd_paths")
        while True:
            while self.sd_scanner_running:
                self.sd_card_manager.updateSDConnectionStatus()
                for sd_path in sd_paths:
                    status = self.sd_card_manager.getConnectionStatus(sd_path)
                    self.setSDCard(status)
                time.sleep(2)  
             
    def toggleSDScanner(self):
        if self.sd_scanner_running:
            self.stopSDScanner()
        else:
            self.startSDScanner()
                
                
    def copyPhotosToBackups(self):
        photo_manager = PhotoManager()
        photo_manager.backupConnectedSDCardsAll()
    
    def copyPhotosToBackupsNew(self):
        photo_manager = PhotoManager()
        photo_manager.backupConnectedSDCardsNew()
                        
                
            
    def wipeSDCard(self):
        properties_manager = PropertiesManager()
        properties_manager.loadProperties()
        sd_cards = properties_manager.getProperty("sd_paths")
        for sd_card in sd_cards:
            connection_status = self.sd_card_manager.getConnectionStatus(sd_card)
            if connection_status:
                result = tkMessageBox.askquestion("Wipe SD Card", "Wipe SD Card " + sd_card + "?", icon='warning')
                if result == 'yes':
                    print "Deleted"
                else:
                    print "I'm Not Deleted Yet"
        
    def loadButtons(self):
        #toggle_sd_card_scanner = Tkinter.Button(self.top, text ="Toggle SD Card Scanner", command = self.toggleSDScanner)
        #toggle_sd_card_scanner.grid(row=1, column=0)
        
        copy_photos_to_backup_dir = Tkinter.Button(self.top, text ="Copy All Photos To Backups", command = self.copyPhotosToBackups)
        copy_photos_to_backup_dir.grid(row=1, column=0)
        
        copy_photos_to_backup_dir_new = Tkinter.Button(self.top, text ="Copy New Photos To Backups", command = self.copyPhotosToBackupsNew)
        copy_photos_to_backup_dir_new.grid(row=2, column=0)

        #wipe_sd_drive = Tkinter.Button(self.top, text ="Wipe SD card", command = self.wipeSDCard)
        #wipe_sd_drive.grid(row=2, column=0)
        
            
                
                
                
      

    def loadGUIWindow(self):
        self.top = Tkinter.Tk()
        self.top.resizable(width=False, height=False)
        self.top.geometry("212x200")

    def startLoop(self):
        self.top.update_idletasks()
        self.top.update()

    def update(self):
        self.top.mainloop()

    def setSDCard(self, toggle):
        if toggle:
            self.sd_image = PhotoImage(file = os.getcwd() + "/images/green_sd.gif")
        else:
            self.sd_image = PhotoImage(file = os.getcwd() + "/images/red_sd.gif")
        if self.sd_card_img == None:
            lbl = Label(self.top, image = self.sd_image)
            lbl.image = self.sd_image  #keeping a reference in this line
            lbl.grid(row=0, column=0)
        else:
            self.canvas.itemconfig(self.sd_card_img, image = self.sd_image)
    
if __name__ == "__main__":
    photo_gui = PhotoSimpleGUI()
    photo_gui.loadGUIWindow()
    photo_gui.loadButtons()
    photo_gui.startThreads()
    photo_gui.startLoop()
    photo_gui.update()