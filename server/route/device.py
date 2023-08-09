from flask import Blueprint
from flask_restful import Api
from controller import SingleDeviceAPI, MultiDeviceAPI, \
    GetMultiDeviceFullInfoAPI, GetSingleDeviceFullInfoAPI, \
        GetMultiDeviceByHomeAPI, GetMultiDeviceByRoomAPI, \
        GetMultiDeviceFullInfoByHomeAPI, GetMultiDeviceFullInfoByRoomAPI, GatewayDeviceAPI

device_api = Blueprint('device_api', __name__)
api = Api(device_api)

api.add_resource(SingleDeviceAPI, '/api/v1/device/<device_id>')
api.add_resource(MultiDeviceAPI, '/api/v1/device')
api.add_resource(GatewayDeviceAPI, '/api/gateway/device/<device_id>')

api.add_resource(GetSingleDeviceFullInfoAPI, '/api/v2/device/<device_id>')
api.add_resource(GetMultiDeviceFullInfoAPI, '/api/v2/device')

api.add_resource(GetMultiDeviceByHomeAPI, '/api/v3/device/home/<home_id>')
api.add_resource(GetMultiDeviceByRoomAPI, '/api/v3/device/room/<room_id>')

api.add_resource(GetMultiDeviceFullInfoByHomeAPI, '/api/v4/device/home/<home_id>')
api.add_resource(GetMultiDeviceFullInfoByRoomAPI, '/api/v4/device/room/<room_id>')
