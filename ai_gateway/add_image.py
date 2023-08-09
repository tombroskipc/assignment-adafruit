import config
import requests

res = requests.post(
    url="http://{}:{}/api/user/{}".format(config.AI_SERVER_HOST, config.AI_SERVER_PORT, 'user00000'),
    files={'file': open('images/tmp.jpg', 'rb')})

res = requests.get(
    url="http://{}:{}/api/user/{}".format(config.AI_SERVER_HOST, config.AI_SERVER_PORT, 'user00000'))

# res = requests.post(
#     url="http://{}:{}/api/predict".format(config.AI_SERVER_HOST, config.AI_SERVER_PORT))
