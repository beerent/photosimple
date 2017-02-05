import os
import sys
import time
import hashlib
from shutil import copy2

from File import File
from Logger import Logger

class FileManager(object):
    accepted_extensions = [".jpg"]
    
    def __init__(self):
        self.none = None
        self.logger = Logger()
         
    def getFiles(self, path):
        files = os.listdir(path)
        
        file_list = []
        for file in files:
            filename = file.lower()
            filepath = "%s%s" % (path, filename)
            if "." not in filename or filename[filename.rindex('.'):] not in self.accepted_extensions:
                self.logger.debug("skipping file '%s'" % filename)
                continue
            
            hash = self.getHash(filepath)
            birth = self.getBirth(filepath)
            file_list.append(File(filename, filepath, birth, hash))
        self.logger.debug("%s accepted files found in directory %s" % (str(len(file_list)), path))
        return file_list
    
    def getBirth(self, file_path):
        epoch = os.stat(file_path).st_birthtime
        datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
        return datetime
    
    def getHash(self, file_path):
        self.logger.debug("generating hash for file '%s'" % file_path)
        BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
        
        sha1 = hashlib.sha1()
        
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha1.update(data)
        self.logger.debug("SHA1 for file '%s': %s" % (file_path, sha1.hexdigest()))
        return sha1.hexdigest()
        
    def copyFile(self, source, destination):
        self.logger.debug("copying file '%s' to destination '%s'"% (source, destination))
        copy2(source, destination)   