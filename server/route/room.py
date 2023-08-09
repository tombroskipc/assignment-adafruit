from flask import Blueprint
from flask_restful import Api
from controller import MultiRoomAPI, SingleRoomAPI, GetRoomByHomeAPI

room_api = Blueprint('room_api', __name__)
api = Api(room_api)

api.add_resource(MultiRoomAPI, '/api/v1/room')
api.add_resource(SingleRoomAPI, '/api/v1/room/<room_id>')

api.add_resource(GetRoomByHomeAPI, '/api/v2/room/home/<home_id>')