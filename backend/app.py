from flask import Flask, request, jsonify, send_file
from main import PhotoAnalysisPipeline
import os
from config import Config
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
pipeline = PhotoAnalysisPipeline()
config = Config()

@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    try:
        results = pipeline.query_photos(query)
        return jsonify({
            "results": [{
                "imagePath": r["imagePath"],
                "timestamp": r["timestamp"],
                "activities": r.get("activities", [])
            } for r in results],
            "query": query
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/image', methods=['GET'])
def get_image():
    image_path = request.args.get('path')
    if not image_path:
        return jsonify({"error": "Path parameter is required"}), 400
    
    # Security checks
    try:
        safe_path = os.path.normpath(image_path)
        if not safe_path.startswith(config.ONEDRIVE_ROOT):
            return jsonify({"error": "Access denied"}), 403
        
        if not os.path.exists(safe_path):
            return jsonify({"error": "Image not found"}), 404
        
        return send_file(safe_path, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/process', methods=['POST'])
def process_images():
    try:
        pipeline.process_onedrive()
        return jsonify({"status": "Processing completed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.SERVER_PORT)