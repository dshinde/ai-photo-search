import React, { useState } from 'react';
import './FaceTagging.css';

function FaceTagging({ imagePath, faces, onTag }) {
  const [currentTag, setCurrentTag] = useState('');
  const [editingFace, setEditingFace] = useState(null);

  const handleTagSubmit = (e) => {
    e.preventDefault();
    if (editingFace !== null && currentTag.trim()) {
      onTag(faces[editingFace], editingFace, currentTag);
      setCurrentTag('');
      setEditingFace(null);
    }
  };

  return (
    <div className="face-tagging-container">
      <div className="image-container">
        <img 
          src={`http://localhost:5000/api/image?path=${encodeURIComponent(imagePath)}`} 
          alt="Selected"
        />
        {faces.map((face, index) => (
          <div 
            key={index}
            className="face-box"
            style={{
              left: `${face.bbox[0]}px`,
              top: `${face.bbox[1]}px`,
              width: `${face.bbox[2] - face.bbox[0]}px`,
              height: `${face.bbox[3] - face.bbox[1]}px`
            }}
            onClick={() => setEditingFace(index)}
          >
            <span className="face-label">{face.name || '?'}</span>
          </div>
        ))}
      </div>

      {editingFace !== null && (
        <form onSubmit={handleTagSubmit} className="tag-form">
          <input
            type="text"
            value={currentTag}
            onChange={(e) => setCurrentTag(e.target.value)}
            placeholder="Enter name"
            autoFocus
          />
          <button type="submit">Save</button>
          <button 
            type="button" 
            onClick={() => {
              setEditingFace(null);
              setCurrentTag('');
            }}
          >
            Cancel
          </button>
        </form>
      )}
    </div>
  );
}

export default FaceTagging;