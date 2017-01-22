import os
import sys
import time
import hashlib
from shutil import copy2

from MD5File import MD5File
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
            filepath = "%s/%s" % (path, filename)
            if "." not in filename or  filename[filename.rindex('.'):] not in self.accepted_extensions:
                continue
            md5 = self.getMD5(filepath)
            birth = self.getBirth(filepath)
            file_list.append(MD5File(filename, filepath, birth, md5))
        self.logger.debug("%s files found in directory %s" % (str(len(file_list)), path))
        return file_list
    
    def getBirth(self, file_path):
        epoch = os.stat(file_path).st_birthtime
        datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
        return datetime
    
    def getMD5(self, file_path):
        self.logger.debug("generating md5 for file '%s'" % file_path)
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
        
    def backupFile(self, source, destination):
        copy2(source, destination)
        
        
            
            