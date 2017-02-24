from QueryResult import QueryResult
from QueryDAO import QueryDAO
from Logger import Logger
from Photo import Photo

class QueryManager():
    
    def __init__(self, database_manager):
        self.query_dao = QueryDAO(database_manager)
        self.logger = Logger()
        
    def queryPhotosRequest(self, added_from, added, added_to, modified_from, modified, modified_to):
        return None
    
    def queryPhotos(self, added_from, added, added_to, modified_from, modified, modified_to):
        self.logger.debug("collecting photos with the following conditions:")
        if added_from is not None:
            self.logger.debug("added from %s" % added_from)
        if added is not None:
            self.logger.debug("added: %s" % added)
        if added_to is not None:
            self.logger.debug("added to: %s" % added_to)
        if modified_from is not None:
            self.logger.debug("modified from: %s" % modified_from)
        if modified is not None:
            self.logger.debug("modified: %s" % modified)
        if modified_to is not None:
            self.logger.debug("modified to: %s" % modified_to)
        results = self.query_dao.queryPhotos(added_from, added, added_to,\
                                            modified_from, modified, modified_to)
        
        photos = []
        
        if results == None:
            self.logger.log("0 photos collected")

        else:
            for result in results:
                id = result[0]
                filename = result[1]
                sub_dir = result[2]
                hash = result[3]
                source = result[4]
                added = result[5]
                modified = result[6]
                photo = Photo(id, filename, sub_dir, hash, source, added, modified)
                photos.append(photo)
            self.logger.debug("%s photos collected" % str(len(photos)))

        return QueryResult(photos, True, None)
   
        