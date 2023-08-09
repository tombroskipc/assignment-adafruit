import config
from datetime import datetime
from database.error import *
import gridfs

class User():
    def __init__(self,
                 username = None,
                 password = None,
                 image_id = None,
                 home_id = None):
        
        self.data = {
            "_id": None,
            "username" : username,
            "password" : password,
            "image_id" : None if image_id is None else [image_id],
            "home_id"  : None if home_id is None else [home_id] 
        }

    def _add_callback_(self, 
                       collection):

        query = {}
        get_id = collection._count_data(config.database.DOC_USER_LIST, query)
        self.data["_id"] = "user{:05d}".format(get_id)
        collection._add_data(config.database.DOC_USER_LIST, self.data)

    def _update_callback_(self, 
                         collection, 
                         updated_data, 
                         query = None, 
                         mode = "first"):
        
        if query is None:
            query = {"_id" : self.data["_id"]}
        
        if not isinstance(updated_data, dict):
            message = "Update data must be form as a dictionary!"
            raise OperationFailed(message)

        for k, v in self.data.items():
            if k in updated_data.keys():
                if k == "image_id" or "home_id":
                    if self.data[k] is None:
                        if isinstance(updated_data[k], list):
                            self.data[k] = updated_data[k]
                        else:
                            self.data[k] = [updated_data[k]]
                    else:
                        if isinstance(updated_data[k], list):
                            self.data[k] + updated_data[k]
                        else:
                            self.data[k].append(updated_data[k])
                else:
                    self.data[k] = updated_data[k]

        collection._update_data(config.database.DOC_USER_LIST, self.data, query, mode)

    def _remove_callback_(self, 
                          collection,
                          query,
                          mode):
        if query is None:
            query = {"_id" : self.data["_id"]}
        collection._remove_data(config.database.DOC_USER_LIST, query, mode)

    def add_face_id(self, 
                    collection,
                    image_id):
        
        query = {"_id" : self.data["_id"]}

        if self.data['image_id'] is None:
            self.data['image_id'] = [image_id]

        else:
            self.data['image_id'].append(image_id)

        collection._update_data(config.database.DOC_USER_LIST, self.data, query)

    def count_image_id(self):
        return str("You have {} id(s) in your image id.".format(0 if self.data['image_id'] is None else len(self.data['image_id'])))

    def load_face_id(self,
                     index):
        if self.data['image_id'] is None:
            message = "No faceID of this User found. Please add a faceID first!"
            raise OperationFailed(message)
        else:
            if index > len(self.data['image_id']):
                message = "This user only has {} id(s). Your query of index: {} is out of range!".format(len(self.data['image_id']), index+1)
                raise OperationFailed("")
            file_id = self.data['image_id'][index]

            return file_id
        

    def load_data(self, 
                  load_data : dict):
        """Load a data dictionary to object"""
        for k,v in self.data.items():
            if k not in load_data.keys():
                message = "Field {} is not available in the loading data!".format(k)
                raise OperationFailed(message)
            if isinstance(v, dict):
                self.data[k].update(load_data[k])
            elif k in load_data.keys():
                self.data[k] = load_data[k]

    def show(self):
        return self.data

class Device():
    def __init__(self,
                 type : str,
                 name : str = None,
                 room_id : str = None,
                 home_id : str = None,                   
                 curr_state : bool = None,              #0: inactive, 1: active
                 curr_value = None,
                 time_activated : str = None,
                 time_deactivated : str = None):

        self.devices = config.database.DEVICE_TYPE_LIST
        self.feed_id = None

        if type not in self.devices:
            message = "Unknown device in this database. Available device are {}".format(i for i in self.devices)
            raise DatabaseException(message)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        if not name:
            names = type.split('-')
            name = ''
            for n in names:
                name += n.capitalize() + ' '

        self.data = {
            "_id" : self.feed_id,
            "type" : type,
            "name" : name,
            "room_id" : room_id,
            "home_id" : home_id,
            "states" : {} if curr_state is None else {dt_string : curr_state},
            "curr_state" : curr_state,
            "state_time" : {} if time_activated is None else {time_activated : time_deactivated},
            "values" : {} if curr_value is None else {dt_string : curr_value},
            "curr_value" : curr_value
        }

    def _add_callback_(self, 
                       collection):
        
        query = {"_id" : self.data["home_id"]}
        exist =  collection._count_data(config.database.DOC_HOME_LIST, query)
        if not exist:
            message = "Id not found in database: {}!".format(self.data["home_id"])
            raise DatabaseException(message)
        
        query = {"_id" : self.data["room_id"]}
        exist =  collection._count_data(config.database.DOC_ROOM_LIST, query)
        if not exist:
            message = "Id not found in database: {}!".format(self.data["room_id"])
            raise DatabaseException(message)

        query = {"type" : self.data["type"]}
        get_id = collection._count_data(config.database.DOC_DEVICE_LIST, query)
        
        self.feed_id = "{}{:05d}".format(self.data["type"],get_id)

        self.data["_id"] = self.feed_id

        collection._add_data(config.database.DOC_DEVICE_LIST, self.data)

    def _update_callback_(self, 
                         collection, 
                         updated_data, 
                         query = None, 
                         mode = "first"):
        
        if query is None:
            query = {"_id" : self.data["_id"]}
        
        if not isinstance(updated_data, dict):
            message = "Update data must be form as a dictionary!"
            raise OperationFailed(message)

        for k, v in self.data.items():
            if k in updated_data.keys():
                if isinstance(v, dict) and isinstance(updated_data[k], dict):
                    self.data[k].update(updated_data[k])

                elif k == "curr_value":
                    self.data[k] = updated_data[k]
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    self.data["values"][dt_string] = updated_data[k]

                elif k == "curr_state":
                    if self.data[k] != updated_data[k]:
                        self.data[k] = updated_data[k]
                        now = datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                        if updated_data[k]:
                            self.data["state_time"][dt_string] = None
                        else:
                            last_ley = list(self.data["state_time"])[-1]
                            self.data["state_time"][last_ley] = dt_string

                else:
                    self.data[k] = updated_data[k]
                
        collection._update_data(config.database.DOC_DEVICE_LIST, self.data, query, mode)

    def _remove_callback_(self, 
                          collection,
                          query,
                          mode):
        if query is None:
            query = {"_id" : self.data["_id"]}
        collection._remove_data(config.database.DOC_DEVICE_LIST, query, mode)
    
    
    def load_data(self, 
                  load_data : dict):
        
        """Load a data dictionary to object"""

        for k,v in self.data.items():
            if k not in load_data.keys():
                message = "Field {} is not available in the loading data!".format(k)
                raise OperationFailed(message)
            if isinstance(v, dict):
                self.data[k].update(load_data[k])
            elif k in load_data.keys():
                self.data[k] = load_data[k]
    
    def load_info(self, 
                  load_data : dict):
        
        """Load a data dictionary to object"""
        try:
            self.data["_id"] = load_data["_id"]
            self.data["type"] = load_data["type"]
            self.data["name"] = load_data["name"]
            self.data["curr_state"] = load_data["curr_state"]
            self.data["curr_value"] = load_data["curr_value"]
            self.data["home_id"] = load_data["home_id"]
            self.data["room_id"] = load_data["room_id"]
        except:
            message = "Field is not available in the loading data!"
            raise OperationFailed(message)


    def show(self):
        return self.data

    def get_log(self):
        return {self.data["states"], self.data["values"]}

class Home():
    def __init__(self,
                 name = None):

        self.data = {
            "_id": None,
            "name" : name,
            "alarm" : None
        }

    def _add_callback_(self, 
                       collection):
        
        query = {}
        get_id = collection._count_data(config.database.DOC_HOME_LIST, query)

        if self.data["name"] is None:
            self.data["name"] = "YoloSmartHome{:05d}".format(get_id)
        
        self.data["_id"] = "home{:05d}".format(get_id)

        collection._add_data(config.database.DOC_HOME_LIST, self.data)

    def _update_callback_(self, 
                         collection, 
                         updated_data, 
                         query = None, 
                         mode = "first"):
        
        if query is None:
            query = {"_id" : self.data["_id"]}
        
        if not isinstance(updated_data, dict):
            message = "Update data must be form as a dictionary!"
            raise OperationFailed(message)

        for k, v in self.data.items():
            if k in updated_data.keys():
                self.data[k] = updated_data[k]

        collection._update_data(config.database.DOC_HOME_LIST, self.data, query, mode)


    def _remove_callback_(self, 
                          collection,
                          query,
                          mode):
        if query is None:
            query = {"_id" : self.data["_id"]}
        collection._remove_data(config.database.DOC_HOME_LIST, query, mode)

    def warning_trigger(self):

        '''Use the log the alarm when it triggered'''

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        if self.data['alarm'] is None:
            self.data['alarm'] = [dt_string]
        else:
            self.data['alarm'].append(dt_string)

    def load_data(self, 
                  load_data : dict):
        
        """Load a data dictionary to object"""
        for k, v in self.data.items():
            if k not in load_data.keys():
                message = "Field {} is not available in the loading data!".format(k)
                raise OperationFailed(message)
            if isinstance(v, dict):
                self.data[k].update(load_data[k])
            elif k in load_data.keys():
                self.data[k] = load_data[k]

    def show(self):
        return self.data

class Room():
    def __init__(self,
                 home_id = None,
                 name = None):

        self.data = {
            "_id": None,
            "home_id" : home_id,
            "name" : name
        }

    def _add_callback_(self, 
                       collection):
        
        query = {"_id" : self.data["home_id"]}
        exist =  collection._count_data(config.database.DOC_HOME_LIST, query)
        if not exist:
            message = "Id not found in database: {}!".format(self.data["home_id"])
            raise DatabaseException(message)
        
        query = {}
        get_id = collection._count_data(config.database.DOC_ROOM_LIST, query)

        if self.data["name"] is None:
            self.data["name"] = "{}.YoloRoom{:05d}".format(self.data["home_id"], get_id)
        
        self.data["_id"] = "room{:05d}".format(get_id)

        collection._add_data(config.database.DOC_ROOM_LIST, self.data)

    def _update_callback_(self, 
                         collection, 
                         updated_data, 
                         query = None, 
                         mode = "first"):
        
        if query is None:
            query = {"_id" : self.data["_id"]}
        
        if not isinstance(updated_data, dict):
            message = "Update data must be form as a dictionary!"
            raise OperationFailed(message)

        for k, v in self.data.items():
            if k in updated_data.keys():
                self.data[k] = updated_data[k]

        collection._update_data(config.database.DOC_ROOM_LIST, self.data, query, mode)


    def _remove_callback_(self, 
                          collection,
                          query,
                          mode):
        if query is None:
            query = {"_id" : self.data["_id"]}
        collection._remove_data(config.database.DOC_ROOM_LIST, query, mode)

    def load_data(self, 
                  load_data : dict):
        
        """Load a data dictionary to object"""

        for k,v in self.data.items():
            if k not in load_data.keys():
                message = "Field {} is not available in the loading data!".format(k)
                raise OperationFailed(message)
            if isinstance(v, dict):
                self.data[k].update(load_data[k])
            elif k in load_data.keys():
                self.data[k] = load_data[k]

    def show(self):
        return self.data