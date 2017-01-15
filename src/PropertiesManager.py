import os

class PropertiesManager():

    def __init__(self):
        self.loadProperties()
    
    
    def loadProperties(self):
        self.properties_array = {}
        with open("/Users/brentryczak/Documents/photosimple/conf/properties.conf") as f:
            contents = f.readlines()
            for line in contents:
                if line[0] == "#":
                    continue
                line = line.strip()
                if line == "":
                    continue

                line = line.split("=")
                self.properties_array[line[0]] = line[1].split(";")
                
    
    def getProperty(self, property_name):
        return self.properties_array[property_name]