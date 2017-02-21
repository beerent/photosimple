from JSONManager import JSONManager
from Logger import Logger

class ErrorManager():
    
    def __init__(self):
        self.json_manager = JSONManager()
    
    def getErrorJSON(self, error):
        root = self.json_manager.createJSONRoot()
        root = self.json_manager.addElement(root, "error", error.getError())
        root = self.json_manager.addElement(root, "request", error.getRequest())
        return self.json_manager.toJSON(root)
        
        
        