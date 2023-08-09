import config
from database import Device
from error import *

class DeviceModel():
    def __init__(self, database):
        self._database = database

    def update_device_data(self, device_id, data):
        try:
            device_list = self.get_device(device_id, include_log=True)
            if len(device_list) < 1:
                raise RecordNotFound(device_id)
            device = device_list[0]
            device.data["curr_value"] = data
            update_data = {"curr_value": data}
            self._database.update_one_data(device, update_data)
        except:
            raise RecordUpdateError(device_id)
        return device

    def get_device(self, device_id=None, include_log=False, room_id=None, home_id=None):
        query = {}
        if device_id:
            query["_id"] = device_id
        if room_id:
            query["room_id"] = room_id
        if home_id:
            query["home_id"] = home_id
            
        try:
            if include_log:
                device_list = self._database.fetch_data(config.database.DOC_DEVICE_LIST, query)
            else:
                device_list = self._database.fetch_device_info(config.database.DOC_DEVICE_LIST, query)
        except:
            raise RecordFindError(device_id)
        
        if device_id and len(device_list) < 1:
            raise RecordNotFound(device_id)
        
        return device_list

    def add_device(self, record):
        try:
            home_id = record['home_id']
            room_id = record['room_id']
            device_type = record['type']
        except:
            raise LackRequestData()
        device = Device(type=device_type, home_id=home_id, room_id=room_id)
        try:
            self._database.add_data(device)
        except:
            raise RecordInsertError(record)
        
        return device

    def delete_device(self, device_id):
        try:
            device_list = self.get_device(device_id)
            if len(device_list) < 1:
                raise RecordNotFound(device_id)
            device = device_list[0]
            self._database.remove_data(device)
        except:
            raise RecordDeleteError(device_id)
        
        return device