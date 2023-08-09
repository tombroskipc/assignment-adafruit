import config
from flask import Flask
from route import predict_api, user_image_api

app = Flask(__name__)
app.register_blueprint(predict_api)
app.register_blueprint(user_image_api)

if __name__=='__main__':
    app.run(config.server.SERVER_HOST, config.server.SERVER_PORT)

# import os
# import requests
# from flask import Flask, request, redirect
# import pickle
# from werkzeug.utils import secure_filename 

# app = Flask(__name__)

# app.config['IMAGE_UPLOADS'] = os.path.join(os.getcwd(), 'static')

# @app.route('/predict',methods=['POST', 'GET'])
# def predict():
#     """Grabs the input values and uses them to make prediction"""
#     if request.method == 'POST':
#         print(os.getcwd()) 
#         image = request.files["file"]
#         if image.filename == '':
#             print("Filename is invalid")
#             return redirect(request.url)

#         filename = secure_filename(image.filename)

#         basedir = os.path.abspath(os.path.dirname(__file__))
#         img_path = os.path.join(basedir, app.config['IMAGE_UPLOADS'], filename)
#         image.save(img_path)
#         res = requests.post("http://torchserve-mar:8080/predictions/mnist", files={'data': open(img_path, 'rb')})
#         prediction = res.json()

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=9696)