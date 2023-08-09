import config
from .arcface import ArcFace

model_arcface = ArcFace(model_path=config.server.MODEL_PATH)