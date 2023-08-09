from flask import Blueprint
from flask_restful import Api
from controller import LoginAPI, UserAPI, UserImageAPI, SignupAPI

login_api = Blueprint('login_api', __name__)
api = Api(login_api)

api.add_resource(LoginAPI, '/login')
api.add_resource(SignupAPI, '/signup')
api.add_resource(UserAPI, '/api/v1/user/<user_id>')
api.add_resource(UserImageAPI, '/api/v1/user_image/<user_id>')