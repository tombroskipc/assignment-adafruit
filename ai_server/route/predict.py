from flask import Blueprint
from flask_restful import Api
from controller import PredictAPI

predict_api = Blueprint('predict_api', __name__)
api = Api(predict_api)

api.add_resource(PredictAPI, '/api/predict')