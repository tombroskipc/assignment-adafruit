import config
from database import Home
from error import *

class HomeModel():
    def __init__(self, database) -> None:
        self._database = database

    def get_home(self, home_id=None):
        query = {}
        if home_id:
            query["_id"] = home_id
        try:
            home_list = self._database.fetch_data(config.database.DOC_HOME_LIST, query)
        except:
            raise RecordFindError(home_id)
        
        if home_id and len(home_list) < 1:
            raise RecordNotFound(home_id)
        
        return home_list
    
    def add_home(self, record):
        try:
            name = record['name']
        except:
            raise LackRequestData()

        home = Home(name)

        try:
            self._database.add_data(home)
        except:
            raise RecordInsertError(record)

        return home


    def delete_home(self, home_id):
        try:
            home_list = self.get_home(home_id)
            if len(home_list) < 1:
                raise RecordNotFound(home_id)
            home = home_list[0]
            self._database.remove_data(home)
        except:
            raise RecordDeleteError(home_id)
        return home
    
    
    def update_warning(self, home_id, alarm):
        try:
            home_list = self.get_home(home_id)
            if len(home_list) < 1:
                raise RecordNotFound(home_id)
            home = home_list[0]
            update_data = {'alarm': alarm}
            self._database.update_one_data(home, update_data)
        except:
            raise RecordUpdateError(home_id)
        return home