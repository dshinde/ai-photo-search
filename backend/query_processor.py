import spacy
from typing import Dict, List
from config import Config
import clip
import torch

class QueryProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.config = Config()
    
    def parse_query(self, query: str) -> Dict[str, str]:
        doc = self.nlp(query)
        
        result = {
            "person": None,
            "location": None,
            "activity": None,
            "date_range": None
        }
        
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                result["person"] = ent.text
            elif ent.label_ in ["GPE", "LOC", "FAC"]:
                result["location"] = ent.text
            elif ent.label_ == "DATE":
                result["date_range"] = ent.text
        
        activity_keywords = {
            "standing": ["standing", "stand"],
            "sitting": ["sitting", "sit"],
            "playing": ["playing", "play"],
            "celebrating": ["celebrating", "celebration"]
        }
        
        for token in doc:
            for activity, keywords in activity_keywords.items():
                if token.lemma_ in keywords:
                    result["activity"] = activity
        
        return result
    
    def get_clip_embedding(self, text: str):
        model, _ = clip.load(self.config.CLIP_MODEL)
        text_input = clip.tokenize([text])
        with torch.no_grad():
            text_features = model.encode_text(text_input)
        return text_features.squeeze(0).tolist()