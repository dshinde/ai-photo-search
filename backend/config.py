import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OneDrive configuration
    ONEDRIVE_ROOT = os.getenv("ONEDRIVE_ROOT", "/path/to/onedrive")
    
    # Model paths
    RETINA_MODEL = "retinaface_resnet50"
    ARCFACE_MODEL = "buffalo_l"
    CLIP_MODEL = "ViT-L/14"
    PLACES365_MODEL = "resnet50_places365"
    
    # Weaviate configuration
    WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "")
    
    # Processing parameters
    BATCH_SIZE = 16
    IMAGE_SIZE = 800
    FACE_THRESHOLD = 0.8
    SERVER_PORT = 5000