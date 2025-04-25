# AI Photo Search System

A complete solution for searching photos by faces, locations, and activities.

## Features
- Face detection and recognition
- Scene understanding with CLIP and Places365
- Activity classification
- Natural language search
- Web interface with face tagging

## Setup

1. **Prerequisites**:
   - Docker and Docker Compose
   - Node.js (for frontend development)
   - Python 3.8+ (for backend)

2. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_lg