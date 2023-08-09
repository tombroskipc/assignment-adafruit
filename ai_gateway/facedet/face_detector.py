import numpy as np
import math
import cv2
from PIL import Image

def findEuclideanDistance(source_representation, test_representation):
    if type(source_representation) == list:
        source_representation = np.array(source_representation)

    if type(test_representation) == list:
        test_representation = np.array(test_representation)

    euclidean_distance = source_representation - test_representation
    euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
    euclidean_distance = np.sqrt(euclidean_distance)
    return euclidean_distance

def load_model():
    import mediapipe as mp
    min_conf = 0.5
    mp_face_detection = mp.solutions.face_detection
    model = mp_face_detection.FaceDetection(min_detection_confidence=min_conf)
    return model

class Mediapipe():
    def __init__(self):
        self.model = load_model()
    
    def detect(self, img):
        results = self.model.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        img_width = img.shape[1]
        img_height = img.shape[0]
        
        if not results.detections:
            return [], (0, img_width, 0, img_height)

        faces = []
        regions = []
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            x = max(int(bbox.xmin * img_width), 0)
            y = max(int(bbox.ymin * img_height), 0)
            w = int(bbox.width * img_width)
            h = int(bbox.height * img_height)

            # Get keypoints
            keypoints = detection.location_data.relative_keypoints
            for keypoint in keypoints:
                keypoint.x = int(keypoint.x * img_width) - x
                keypoint.y = int(keypoint.y * img_height) - y

            face = img[y : y + h, x : x + w]
            face = self.align(face, keypoints)
            faces.append(face)
            regions.append((x, x + w, y, y + h))

        return faces, regions


    def align(self, img, keypoints):
        left_eye = (keypoints[1].x, keypoints[1].y)
        right_eye = (keypoints[0].x, keypoints[0].y)
        left_eye_x, left_eye_y = left_eye
        right_eye_x, right_eye_y = right_eye

        if left_eye_y > right_eye_y:
            point_3rd = (left_eye_x, right_eye_y)
            direction = 1 
        else:
            point_3rd = (right_eye_x, left_eye_y)
            direction = -1
        
        a = findEuclideanDistance(np.array(left_eye), np.array(point_3rd))
        b = findEuclideanDistance(np.array(right_eye), np.array(point_3rd))
        c = findEuclideanDistance(np.array(right_eye), np.array(left_eye))

        if b != 0 and c != 0:
            cos_a = (b * b + c * c - a * a) / (2 * b * c)
            angle = np.arccos(cos_a)
            angle = (angle * 180) / math.pi
            if direction == -1:
                angle = 90 - angle

            img = Image.fromarray(img)
            img = np.array(img.rotate(direction * angle))
        
        return img 