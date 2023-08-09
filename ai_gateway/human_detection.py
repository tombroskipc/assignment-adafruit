import cv2
import time
import dropbox
import torch
import datetime
import requests
import numpy as np
import base64
import config

class HumanDetection():
    def __init__(self, source=0):
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5n", pretrained=True)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.source = source
        self.threshold = 0.5
        self.frame_width = 720
        self.frame_height = 405
        self.is_warning_sent = False
        self.send_start_time = 0
        self.send_duration = 30
        self.record_time = 4

    def set_stream(self):
        self.cap = cv2.VideoCapture(self.source)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.cap.set(cv2.CAP_PROP_FPS, 15)

    def get_labels_coords(self, results):
        return results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()

    def check_human(self, labels):
        return 0 in labels

    def plot_bboxes(self, frame, coords):
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for coord in coords:
            if coord[4] > self.threshold:
                row = coord[:4]
                x0, y0, x1, y1 = row[0], row[1], row[2], row[3]
                x0, y0, x1, y1 = int(row[0]*x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(row[3] * y_shape)
                cv2.rectangle(frame, (x0, y0), (x1, y1), (255, 127, 128), 2)
    
        return frame
    
    def send_warning(self):
        data = {
            'data': 1
        }

        if self.is_warning_sent:
            return
        
        try:
            dbx = dropbox.Dropbox(config.DBX_TOKEN)
            vid_file = 'images/tmp.mp4'
            with open(vid_file, "rb") as f:
                meta = dbx.files_upload(f.read(), '/Videos/tmp.mp4', mode=dropbox.files.WriteMode("overwrite"))
        except Exception as err:
            print('Cannot push video: ', err)

        try:
            res = requests.put(
                url="http://{}:{}/api/gateway/device/{}".format(config.SERVER_HOST, config.SERVER_PORT, config.WARNING_ID),
                data=data)
        except Exception as err:
            print('Cannot send request: ', err)
        
        self.is_warning_sent = True
        self.send_start_time = time.time()
        
        return res.json()

    def run(self):
        self.set_stream()
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('images/{}.mp4'.format('tmp'), fourcc, 15.0, (self.frame_width, self.frame_height))
        human_detected = False
        while (True):
            ret, frame = self.cap.read()

            if not ret:
                break

            frame = cv2.resize(frame, (self.frame_width, self.frame_height))

            results = self.model(frame)
            labels, coords = self.get_labels_coords(results)

            frame = self.plot_bboxes(frame, coords)
            cv2.imshow('video', frame)

            if self.check_human(labels):
                if not human_detected:
                    start_time = time.time()
                    human_detected = True

            if human_detected:
                end_time = time.time()
                if end_time - start_time < self.record_time:
                    stack = np.hstack([frame])
                    out.write(stack)
                else:
                    res = self.send_warning()
            
            curr = time.time()

            if curr - self.send_start_time > self.send_duration and self.is_warning_sent:
                self.is_warning_sent = False
                human_detected = False

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__=='__main__':
    human_detection = HumanDetection('images/hd_demo.mp4')
    human_detection.run()