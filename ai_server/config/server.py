import os
from dotenv import load_dotenv

load_dotenv()

SERVER_HOST = os.getenv('AI_SERVER_HOST')
SERVER_PORT = os.getenv('AI_SERVER_PORT')
SECRET_KEY = os.getenv('SECRET_KEY')
MODEL_PATH = 'ckpts/resnet18_110.pth'