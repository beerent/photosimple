import hashlib
from pathlib import Path

class MD5Manager(object):
    def __init__(self):
        nothing = 1
    
    def generateMD5OfFile(self, filepath):
        if not Path(filepath).is_file():
            raise_message = "[ERROR] (MD5Manager.geterateMD5OfFile) file '%s' is not a file." % (filepath,)
            print(raise_message)
            return None
        
        return hashlib.md5(open(filepath.replace("\\ ", " "),'rb').read()).hexdigest()