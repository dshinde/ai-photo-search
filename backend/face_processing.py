import cv2
import torch
from retinaface import RetinaFace
from insightface.app import FaceAnalysis
from typing import List, Dict, Any
from config import Config

class FaceProcessor:
    def __init__(self):
        self.config = Config()
        self.retina_detector = RetinaFace.build_model()
        self.arcface = FaceAnalysis(name=self.config.ARCFACE_MODEL)
        self.arcface.prepare(ctx_id=0)
    
    def detect_faces(self, image_path: str) -> List[Dict[str, Any]]:
        img = cv2.imread(image_path)
        img = cv2.resize(img, (self.config.IMAGE_SIZE, self.config.IMAGE_SIZE))
        
        faces = RetinaFace.detect_faces(img, threshold=self.config.FACE_THRESHOLD)
        
        results = []
        if isinstance(faces, dict):
            for face_id, face_data in faces.items():
                x1, y1, x2, y2 = face_data['facial_area']
                face_img = img[y1:y2, x1:x2]
                face_embedding = self.arcface.get(face_img)[0]['embedding']
                
                results.append({
                    'bbox': face_data['facial_area'],
                    'landmarks': face_data['landmarks'],
                    'embedding': face_embedding.tolist(),
                    'confidence': face_data['score']
                })
        
        return results