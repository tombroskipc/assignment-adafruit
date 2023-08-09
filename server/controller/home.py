import json
from flask import request
from flask_restful import Resource
from database import iot_database
from model import adafruit_server, home_model
from controller.response import create_response
from middleware import token_require
from error import *

class MultiHomeAPI(Resource):
    def __init__(self, **kwargs) -> None:
        super(Resource, self).__init__()

    @token_require
    def get(self):
        try:
            home_list = home_model.get_home()
        except Exception as err:
            return create_response('', err)
        data = [home.data for home in home_list]
        return create_response(data)
        
    @token_require
    def post(self):
        record = request.form.to_dict()
        try:
            home = home_model.add_home(record)
        except Exception as err:
            return create_response('', err)
            
        group_key = home.data["_id"]
        group_name = home.data["name"]
        try:
            adafruit_server.add_group(group_name=group_name, group_key=group_key)
        except:
            create_response('', AdafruitError())
        
        return create_response(home.data)
            
class SingleHomeAPI(Resource):
    def __init__(self, **kwargs) -> None:
        super(Resource, self).__init__()

    @token_require
    def get(self, home_id):
        try:
            home_list = home_model.get_home(home_id)
        except Exception as err:
            return create_response('', err)
        data = [home.data for home in home_list]
        return create_response(data)

    def put(self, home_id):
        record = request.form.to_dict()
        try:
            alarm_info = record['alarm']
        except:
            return create_response('', LackRequestData())
        
        try:
            home = home_model.update_warning(home_id, alarm_info)
        except:
            raise RecordUpdateError()
        
        return create_response(home.data)

    @token_require
    def delete(self, home_id):
        try:
            home = home_model.delete_home(home_id)
        except Exception as err:
            return create_response('', err)
        
        group_key = home.data["_id"]
        try:
            adafruit_server.delete_group(group_key=group_key)
        except:
            return create_response('', AdafruitError())
        
        return create_response(home.data)
        