from flask import Blueprint
from flask_restful import Api
from controller import UserImageAPI

user_image_api = Blueprint('user_image_api', __name__)
api = Api(user_image_api)

api.add_resource(UserImageAPI, '/api/user/<user_id>')