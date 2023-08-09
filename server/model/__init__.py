import config
from database import iot_database
from model.adafruit import Adafruit, AdafruitMQTT
from model.home import HomeModel
from model.room import RoomModel
from model.device import DeviceModel
from model.user import UserModel

device_model = DeviceModel(iot_database)
home_model = HomeModel(iot_database)
room_model = RoomModel(iot_database)
user_model = UserModel(iot_database)

adafruit_server = Adafruit(config.server.ADA_USER, config.server.ADA_KEY)