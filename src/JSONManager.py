import json

class JSONManager():
    
#    def __init__(self):
        
    def createJSONRoot(self):
        return {}
    
    def addElement(self, root, element_name, element):
        root['element_name'] = element
        return root
    
    def toJSON(self, root):
        return json.dumps(root)
    
    def toMap(self, root):
        return json.loads(root)