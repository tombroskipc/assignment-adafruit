import os
import cv2
import time
import torch
import config
from PIL import Image
from facedet import Mediapipe
import requests
import io

class FaceDetection():
    def __init__(self, source=0):
        self.model = Mediapipe()
        self.source = source

    def send_data(self):
        try:
            res = requests.post(
                url="http://{}:{}/api/predict".format(config.AI_SERVER_HOST, config.AI_SERVER_PORT),
                files={'file': open('images/tmp.jpg', 'rb')},
                data={'home_id': config.HOME_ID})
            return res.json()
        except Exception:
            print("Error sending data to AI server")
            return False

    def open_door(self):
        try:
            res = requests.put(
                url="http://{}:{}/api/gateway/device/{}".format(config.SERVER_HOST, config.SERVER_PORT, config.DOOR_ID),
                data={'data': 1})
            return res.json()
        except Exception:
            print("Error sending data to server")
            return False

    def run(self):
        self.capture = cv2.VideoCapture(self.source)
        cap_w = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        cap_h = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        w = int(cap_w * 0.6)
        h = int(cap_h * 0.8)
        x = int((cap_w - w) / 2)
        y = int((cap_h - h) / 2)
        in_area = 0.2 * w * h

        in_frame_time = 3
        frame_include_face = False
        in_frame_tic = time.time()

        while True:
            success, frame = self.capture.read()
            if not success:
                break

            x0, y0, x1, y1 = x, y, x + w, y + h
            cv2.rectangle(frame, (x0, y0), (x1, y1), (255, 127, 128), 2)
            cv2.imshow('video', frame)

            img_frame = frame[y : y + h, x : x + w]

            detected_faces, regions = self.model.detect(img_frame)
            detected_faces_len = len(detected_faces)
            
            if detected_faces_len == 0:
                in_frame_tic = time.time()
            
            if detected_faces_len > 0:
                face = detected_faces[0]
                if (face.shape[0] * face.shape[1] > in_area):
                    in_frame_toc = time.time()
                    if (in_frame_toc - in_frame_tic > in_frame_time):
                        frame_include_face = True
                else:
                    in_frame_tic = time.time()

            if frame_include_face:
                face = detected_faces[0]
                cv2.imwrite('images/tmp.jpg', face)
                try:
                    res = self.send_data()
                    if res['user_id']:
                        if self.open_door():
                            break
                except:
                    print('Cannot send request')
                in_frame_tic = time.time()
                frame_include_face = False
        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.capture.release()
        cv2.destroyAllWindows()
