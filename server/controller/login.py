
import io
import uuid
import json
import jwt
import config
import base64
import requests
from PIL import Image
from bson import json_util
from datetime import datetime, timedelta
from flask_restful import Resource
from flask import Blueprint, request, jsonify
from middleware import token_require
from database import iot_database
from model import user_model
from werkzeug.security import generate_password_hash, check_password_hash
from controller.response import create_response
from error import *

def parse_json(data):
    return json.loads(json_util.dumps(data))

class LoginAPI(Resource):
    def post(self):
        record = request.form.to_dict()
        print(record)
        try:
            username = record['username']
            password = record['password']
        except:
            return create_response('', LackRequestData())     
        
        try:
            user_list = user_model.get_user(username=username)
        except Exception as err:
            return create_response('', err)
        
        user = user_list[0]
        # if check_password_hash(user.data['password'], password):
        if user.data['password'] == password:
            token = jwt.encode({
                'public_id': user.data['_id'],
                'exp' : datetime.utcnow() + timedelta(minutes=90)
            }, config.server.SECRET_KEY)
            return create_response(data=parse_json(user.data), token=token, code=201)

        return create_response('', AccessForbidden("Login not successful"))

class UserAPI(Resource):
    @token_require
    def get(self, user_id):
        try:
            user_list = user_model.get_user(user_id)
        except Exception as err:
            return create_response('', err)
        data = [user.data for user in user_list]
        return create_response(parse_json(data))

    @token_require
    def delete(self, user_id):
        try:
            user = user_model.delete_user(user_id)
        except Exception as err:
            return create_response('', err)
        
        return create_response(parse_json(user.data))
    
    @token_require
    def put(self, user_id):
        record = request.form.to_dict()
        try:
            home_id = record["home_id"]
        except:
            return create_response('', LackRequestData())
        
        try:
            user = user_model.update_user_home(user_id, home_id)
        except Exception as err:
            return create_response('', err)
        
        return create_response(parse_json(user.data))

class UserImageAPI(Resource):
    @token_require
    def put(self, user_id):
        try:
            file = request.files['file']
        except:
            LackRequestData()
        
        resp = requests.post(
            url='http://{}:{}/api/user/{}'.format(config.server.AI_SERVER_HOST, config.server.AI_SERVER_PORT, user_id),
            files={'file': file}
        )

        image_bytes = resp.json()['image']
        image = Image.open(io.BytesIO(base64.b64decode(image_bytes)))
        file_path = 'tmp/tmp.jpg'
        image.save(file_path)
        user_model.update_user_image(user_id, file_path)
        user = user_model.get_user(user_id)[0]
        return create_response(parse_json(user.data))
        
class SignupAPI(Resource):
    @token_require
    def post(self):
        record = request.form.to_dict()        
        try:
            user = user_model.add_user(record)
        except Exception as err:
            return create_response('', err)
        
        return create_response(parse_json(user.data))