import os
import io
import json
import config
import base64
from PIL import Image
from flask import request, jsonify
from flask_restful import Resource
from database import iot_database
from model import model_arcface

import torchvision.transforms as T

def get_user(user_id):
    query = {'_id': user_id}
    user_list = iot_database.fetch_data(config.database.DOC_USER_LIST, query)
    return user_list[0]

class UserImageAPI(Resource):
    def post(self, user_id):
        file = request.files['file']
        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes))
        faces, regions = model_arcface.detect(image)
        if len(faces) < 1:
            return jsonify({'error': 'Cannot detect face'}), 400
        tensor = faces[0]
        image = T.ToPILImage()(tensor)
        img_io = io.BytesIO()
        image.save(img_io, 'JPEG')
        img_str = base64.b64encode(img_io.getvalue()).decode("utf-8")
        return jsonify({'status': True, 'image': img_str})
    
    def get(self, user_id):
        user = get_user(user_id)
        img_bytes = iot_database.load_faceid(user, 0)
        image = Image.open(io.BytesIO(img_bytes))   
        img_io = io.BytesIO()
        image.save(img_io, 'JPEG')
        img_str = base64.b64encode(img_io.getvalue()).decode("utf-8")
        return jsonify({'status': True, 'image': img_str})     