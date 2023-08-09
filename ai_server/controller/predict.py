import os
import io
import json
import config
from PIL import Image
from flask import request, jsonify
from flask_restful import Resource
from database import iot_database, User
from model import model_arcface

def get_user(home_id):
    query = {'home_id': home_id}
    user_list = iot_database.fetch_data(config.database.DOC_USER_LIST, query)
    return user_list

class PredictAPI(Resource):
    def post(self):
        file = request.files['file']
        home_id = request.form['home_id']
        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes))
        user_list = get_user(home_id)
        dists = {}
        for user in user_list:
            img_bytes = iot_database.load_faceid(user, 0)
            user_image = Image.open(io.BytesIO(img_bytes))
            res, distance = model_arcface.verify(image, user_image)
            dists[user.data['_id']] = distance
        
        if not dists:
            return jsonify({'user_id': None, 'distance': '-1'})
        
        user_id = min(dists, key=dists.get)
        return jsonify({'user_id': user_id, 'distance': str(dists[user_id])})