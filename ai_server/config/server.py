import os
from dotenv import load_dotenv

load_dotenv()

SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_PORT = os.getenv('SERVER_PORT')
SECRET_KEY = os.getenv('SECRET_KEY')
MODEL_PATH = 'ckpts/resnet18_110.pth'