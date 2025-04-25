# AI Photo Search - Backend Service

Python Flask backend with computer vision models for face detection, scene recognition, and activity classification.

## Features
- **Face Processing**: RetinaFace detection + ArcFace recognition
- **Scene Understanding**: CLIP + Places365 models
- **Vector Search**: Weaviate integration
- **REST API**: Flask endpoints for processing and search
- **OneDrive Integration**: Local filesystem access to OneDrive photos

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/search` | POST | Process natural language queries |
| `/api/image` | GET | Retrieve processed images |
| `/api/process` | POST | Initiate image processing pipeline |

## Models Used

1. **Face Detection**:
   - Model: RetinaFace (ResNet50 backbone)
   - Output: Bounding boxes + 5 facial landmarks

2. **Face Recognition**:
   - Model: ArcFace (buffalo_l)
   - Output: 512-dimension face embeddings

3. **Scene Understanding**:
   - Model: CLIP (ViT-L/14)
   - Output: 768-dimension image embeddings

4. **Place Recognition**:
   - Model: ResNet50-Places365
   - Output: Top 5 place categories

## Setup Instructions

### 1. Prerequisites
```bash
python==3.8+
pip==20+