import os
from datetime import datetime
from config import Config
from face_processing import FaceProcessor
from scene_activity import SceneActivityRecognizer
from database import VectorDatabase
from query_processor import QueryProcessor
from typing import List, Dict

class PhotoAnalysisPipeline:
    def __init__(self):
        self.config = Config()
        self.face_processor = FaceProcessor()
        self.scene_recognizer = SceneActivityRecognizer()
        self.database = VectorDatabase()
        self.query_processor = QueryProcessor()
    
    def process_image(self, image_path: str):
        faces = self.face_processor.detect_faces(image_path)
        scene_embedding = self.scene_recognizer.get_scene_embedding(image_path)
        place_category = self.scene_recognizer.get_place_category(image_path)
        
        activities = ["standing", "sitting", "playing tennis", "celebrating"]
        activity_probs = self.scene_recognizer.detect_activity(image_path, activities)
        
        photo_data = {
            "image_path": image_path,
            "timestamp": datetime.fromtimestamp(os.path.getmtime(image_path)),
            "faces": faces,
            "scene_embedding": scene_embedding,
            "place_category": place_category,
            "activities": activity_probs
        }
        
        self.database.index_photo(photo_data)
    
    def process_onedrive(self):
        for root, _, files in os.walk(self.config.ONEDRIVE_ROOT):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(root, file)
                    try:
                        self.process_image(image_path)
                    except Exception as e:
                        print(f"Error processing {image_path}: {str(e)}")
    
    def query_photos(self, query: str) -> List[Dict]:
        parsed_query = self.query_processor.parse_query(query)
        query_embedding = self.query_processor.get_clip_embedding(query)
        
        filters = {}
        if parsed_query["person"]:
            filters["persons"] = parsed_query["person"]
        
        results = self.database.search_photos(query_embedding, filters)
        
        if parsed_query["activity"]:
            results = [r for r in results 
                      if parsed_query["activity"] in r.get("activities", [])]
        
        return results