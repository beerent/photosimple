class SDCard(object):
    
    def __init__(self, sd_card_id, sd_name, sd_path):
        self.sd_card_id = sd_card_id
        self.sd_name = sd_name
        self.sd_path = sd_path
    
    def getID(self):
        return self.sd_card_id
    
    def getName(self):
        return self.sd_name
    
    def getPath(self):
        return self.sd_path