from pymongo import MongoClient
from database.document import *
from database.error import DatabaseException
import config
import gridfs


class Database():
    def __init__(self, connection_string):
        
        # Connect to Atlas server
        self.client = MongoClient(connection_string)

        # Initial a database if it has not created yet
        self.collection_name = config.database.DOCUMENT_LIST
        self.instance = (Home, Device, Room, User)
        self.mapping = {
            self.collection_name[0] : Home,
            self.collection_name[1] : Device,
            self.collection_name[2] : Room,
            self.collection_name[3] : User,
        }
        self.database = self.client['IOT_database']

    def add_data(self, object):
        """Add an object to database"""
        if not isinstance(object, self.instance):
             message = "Unknow document in this database!"
             raise OperationFailed(message)

        object._add_callback_(self)

    def add_many_data(self, object_list):
        """Add many object to database"""
        if not isinstance(object_list, list):
            message = "Many of objects must be formed as a list type!"
            raise OperationFailed(message)
        
        for object in object_list:

            if not isinstance(object, self.instance):
                message = "Unknow document in this database!"
                raise OperationFailed(message)
            
            object._add_callback_(self)

    def update_one_data(self, 
                        object, 
                        data, 
                        query = None):
         
        return object._update_callback_(self, data, query, "first")
    
    def update_all_data(self, 
                        object, 
                        data, 
                        query = None):
         
        return object._update_callback_(self, data, query, "many")

    def remove_data(self, 
                    object, 
                    query = None,
                    mode = "first"):
        
        object._remove_callback_(self, query, mode)

    def fetch_data(self, 
                  collection, 
                  query = {}):

        object = self.mapping[collection]
        result = []
        found_data = self._find_data(collection, query)

        for data in found_data:
            if (object == Device):
                res = object(data["type"])
            else:
                res = object()

            res.load_data(data)
            result.append(res)
        return result

    def fetch_device_info(self, 
                  collection,
                  query = {}):
        object = self.mapping[collection]
        result = []
        found_data = self._find_data(collection, query)

        for data in found_data:
            if (object == Device):
                res = object(data["type"])
            else:
                res = object()

            res.load_info(data)
            result.append(res)
        return result

    def _find_data(self, 
                   collection, 
                   query):
        
        return self.database[collection].find(query)
    
    def _count_data(self, 
                    collection, 
                    query):
        
        return self.database[collection].count_documents(query)

    def _add_data(self, 
                  collection, 
                  data):
        """Add a data to collection"""
        if collection in self.collection_name:
                self.database[collection].insert_one(data)
                print("Added data to collection {}".format(collection))
        else:
            message = "Unknown collection in database: {}".format(collection)
            raise DatabaseException(message)

    def _update_data(self, 
                     collection, 
                     data, 
                     query, 
                     mode = "first"):
        data = {"$set": data}
        if mode == "first":
            self.database[collection].update_one(query, data)
        elif mode == "many":
            self.database[collection].update_many(query, data)
        else:
            message = """Invalid update mode: {}, mode must be 'first' or 'many'!""".format(mode)
            raise OperationFailed(message)
            
    def _remove_data(self, 
                     collection, 
                     query,
                     mode = "first"):
        if mode == "first":
            self.database[collection].delete_one(query)
        elif mode == "many":
            self.database[collection].delete_many(query)
        else:
            message = """Invalid remove mode: {}, mode must be 'first' or 'many'!""".format(mode)
            raise OperationFailed(message)
        
    def drop_collection(self, 
                        name):
        
        if name in self.collection_name:
            self.database.drop_collection(name)
        else:
            message = "Unknown collection in database: {}".format(name)
            raise DatabaseException(message)

    def take_action(self, 
                    user,
                    device,
                    command : str = "Do something"):
        
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        command_log = {
            "_id" : dt_string,
            "user_id" : user.show()["_id"],
            "device_id" : device.show()["_id"],
            "command" : command
        }

        self._add_data(config.database.DOC_USAGES, command_log)

    def update_faceid(self,
                      user: User,
                      image):
        
        """Give a image path, this function will read this image and save it to database"""

        if not isinstance(user, User):
            message = "The faceID must be add to User entity only!"
            raise EntityException(message)
        try:
            with open(image, 'rb') as image_file:
                image_data = image_file.read()
        except:
            message = "Image file path not found. Check your image path again!"
            raise OperationFailed(message)
        
        fs = gridfs.GridFS(self.database, collection="images")

        file_id = fs.put(image_data)

        user.add_face_id(self, file_id)

    def load_faceid(self,
                    user : User,
                    index):
        
        """Load face image from user and return binary string of this image"""

        if not isinstance(user, User):
            message = "The faceID must be add to User entity only!"
            raise EntityException(message)
        
        fs = gridfs.GridFS(self.database, collection="images")

        file_id = user.load_face_id(index)

        image_file = fs.get(file_id)

        return image_file.read()


    def list_collection_names(self):
        return self.database.list_collection_names()