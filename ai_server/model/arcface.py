import os
import io
import pickle
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
from pathlib import Path
from utils import load_model

import torch
import torch.nn as nn
from torchvision import transforms
from .resnet import arcface18
from facedet import Mediapipe


class ArcFace(nn.Module):
    def __init__(self, model_path=None):
        super(ArcFace, self).__init__()
        self.model_path = model_path
        self.load_model()

    # def build_database(self, database_path, embed_path):
    #     if self.embed_path:
    #         return
        
    #     file_name = 'embedding.pkl'
    #     if os.path.exists(os.path.join(embed_path, file_name)):
    #         f = open(os.path.join(embed_path, file_name), 'rb')
    #         embeddings = pickle.load(f)
        
    #     employees = []
    #     ids = []
    #     for rt, dr, fs in os.walk(database_path):
    #         for file in fs:
    #             if ('.jpg' in file.lower()) or ('.png' in file.lower()):
    #                 exact_path = os.path.join(rt, file)
    #                 employees.append(exact_path)
    #                 id = rt.split('/')[-1]
    #                 ids.append(id)

    #     if len(employees) == 0:
    #         raise ValueError("There is no image in {} folder! Validate .jpg or .png files exist in this path.".format(database_path))
        
    #     embeddings = []
    #     pbar = tqdm(range(0, len(employees)), desc='Building embeddings')
        
    #     for index in pbar:
    #         employee = employees[index]
    #         img = Image.open(employee).convert('L')
    #         embeddings.append([ids[index], self.forward(img)])
        
    #     Path(embed_path).mkdir(parents=True, exist_ok=True)
    #     self.embed_path = os.path.join(embed_path, file_name)
    #     embed_file = open(self.embed_path, 'wb')
    #     pickle.dump(embeddings, embed_file)
    #     embed_file.close()

    # def find(self, vect, threshold=0.2, top_rows=5):
    #     if not self.embed_path:
    #         raise FileNotFoundError("There is no database embedding file. Please build database first by calling: build_database()") 

    #     embed_file = open(os.path.join(self.embed_path, 'embedding.pkl'), 'rb')
    #     embeddings = pickle.load(embed_file)
    #     df = pd.DataFrame(embeddings, columns=['identity', 'embedding'])
    #     distances = []
    #     for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    #         src_rep = row['embedding']
    #         dist = self.cosine_metric(vect, src_rep)
    #         distances.append(dist)

    #     df['distance'] = distances
    #     df = df.drop(columns=['embedding'])
    #     df = df[df['distance'] <= threshold]
    #     df = df.sort_values(by = ['distance'], ascending=True).reset_index(drop=True)
    #     n_rows = min(len(df.index), top_rows)
    #     return df.head(n_rows)

    def find(self, image):
        return self.forward(image)

    def verify(self, image1, image2, threshold=0.95):
        embed1 = self.forward(image1)
        embed2 = self.forward(image2)

        distance = self.cosine_metric(embed1, embed2)
        
        res = True if distance > threshold else False
        return res, distance

    def load_model(self):
        self.detector = Mediapipe()
        self.model = arcface18()
        load_model(self.model, self.model_path)
        self.model.eval()

    def cosine_metric(self, x1, x2):
        x1 = np.squeeze(x1.detach().numpy())
        x2 = np.squeeze(x2.detach().numpy())
        return np.dot(x1, x2) / (np.linalg.norm(x1) * np.linalg.norm(x2))
    
    def preprocess(self, image):
        self.image_processing = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((128, 128)),
            transforms.ToTensor()
        ])
        return self.image_processing(image).unsqueeze(0)
        
    def forward(self, image):
        return self.model(self.preprocess(image))
    
    def detect(self, image):
        return self.detector.detect(np.array(image))