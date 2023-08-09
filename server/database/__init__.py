import config
from database.database import Database
from database.document import Device, User, Home, Room

iot_database = Database(config.database.DB_KEY)