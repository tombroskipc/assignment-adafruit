import os
from dotenv import load_dotenv

load_dotenv()

SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_PORT = os.getenv('SERVER_PORT')
AI_SERVER_HOST = os.getenv('AI_SERVER_HOST')
AI_SERVER_PORT = os.getenv('AI_SERVER_PORT')
HOME_ID = os.getenv('HOME_ID')
DOOR_ID = os.getenv('DOOR_ID')
LED_ID = os.getenv('LED_ID')
FAN_ID = os.getenv('FAN_ID')
WARNING_ID = os.getenv('WARNING_ID')
DBX_TOKEN = os.getenv('DBX_TOKEN')