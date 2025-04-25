import weaviate
from weaviate.util import generate_uuid5
from typing import List, Dict, Any
from config import Config
import datetime

class VectorDatabase:
    def __init__(self):
        self.config = Config()
        self.client = weaviate.Client(
            url=self.config.WEAVIATE_URL,
            auth_client_secret=weaviate.auth.AuthApiKey(self.config.WEAVIATE_API_KEY)
        )
        self._create_schema()
    
    def _create_schema(self):
        schema = {
            "classes": [
                {
                    "class": "Photo",
                    "properties": [
                        {"name": "imagePath", "dataType": ["string"]},
                        {"name": "timestamp", "dataType": ["date"]},
                        {"name": "persons", "dataType": ["Person"]},
                        {"name": "placeCategory", "dataType": ["int[]"]},
                        {"name": "activities", "dataType": ["string[]"]}
                    ],
                    "vectorIndexType": "hnsw"
                },
                {
                    "class": "Person",
                    "properties": [
                        {"name": "name", "dataType": ["string"]},
                        {"name": "faceEmbedding", "dataType": ["number[]"]}
                    ]
                }
            ]
        }
        self.client.schema.create(schema)
    
    def index_photo(self, photo_data: Dict[str, Any]):
        timestamp = photo_data["timestamp"]
        if isinstance(timestamp, datetime.datetime):
            timestamp = timestamp.isoformat()
        
        photo_obj = {
            "imagePath": photo_data["image_path"],
            "timestamp": timestamp,
            "placeCategory": photo_data["place_category"],
            "activities": list(photo_data["activities"].keys())
        }
        
        photo_id = self.client.data_object.create(
            data_object=photo_obj,
            class_name="Photo",
            vector=photo_data["scene_embedding"]
        )
        
        for face in photo_data["faces"]:
            person_obj = {
                "name": face.get("name", "unknown"),
                "faceEmbedding": face["embedding"]
            }
            person_id = self.client.data_object.create(
                data_object=person_obj,
                class_name="Person"
            )
            
            self.client.data_object.reference.add(
                from_class_name="Photo",
                from_uuid=photo_id,
                from_property_name="persons",
                to_class_name="Person",
                to_uuid=person_id
            )
    
    def search_photos(self, query_embedding: List[float], filters: Dict = None):
        query = {
            "vector": query_embedding,
            "limit": 20,
            "withCertainty": True
        }
        
        if filters:
            where_clause = {"operator": "And", "operands": []}
            
            if "persons" in filters:
                where_clause["operands"].append({
                    "path": ["persons", "Person", "name"],
                    "operator": "Equal",
                    "valueString": filters["persons"]
                })
            
            if "dateRange" in filters:
                where_clause["operands"].append({
                    "path": ["timestamp"],
                    "operator": "GreaterThanEqual",
                    "valueDate": filters["dateRange"]["start"]
                })
                where_clause["operands"].append({
                    "path": ["timestamp"],
                    "operator": "LessThanEqual",
                    "valueDate": filters["dateRange"]["end"]
                })
            
            query["where"] = where_clause
        
        result = self.client.query.get(
            "Photo",
            ["imagePath", "timestamp", "activities"]
        ).with_near_vector(query).do()
        
        return result.get("data", {}).get("Get", {}).get("Photo", [])