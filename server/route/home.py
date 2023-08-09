from flask import Blueprint
from flask_restful import Api
from controller import MultiHomeAPI, SingleHomeAPI

home_api = Blueprint('home_api', __name__)
api = Api(home_api)

api.add_resource(MultiHomeAPI, '/api/v1/home')
api.add_resource(SingleHomeAPI, '/api/v1/home/<home_id>')