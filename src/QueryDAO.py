class QueryDAO():

    def __init__(self, database_manager):
        self.database_manager = database_manager
        
    def queryPhotos(self, added_from, added, added_to, modified_from, modified, modified_to):
        vars = []
                
        sql = "select * from photos where 1=1 "
        if added_from is not None:
            sql = sql + "and added > %s "
            vars.append(added_from)
        if added is not None:
            sql = sql + "and added > %s "
            sql = sql + "and added < %s + interval 1 day "
            vars.append(added)
            vars.append(added)
        if added_to is not None:
            sql = sql + "and added < %s + interval 1 day "
            vars.append(added_to)
        if modified_from is not None:
            sql = sql + "and modified > %s "
            vars.append(modified_from)
        if modified is not None:
            sql = sql + "and modified > %s "
            sql = sql + "and modified < %s + interval 1 day "
            vars.append(modified)
            vars.append(modified)
        if modified_to is not None:
            sql = sql + "and modified < %s + interval 1 day "
            vars.append(modified_to)
            
        vars = tuple(vars)
        
        res = self.database_manager.execute(sql, vars)
        if len(res) == 0:
            return None
        
        return res