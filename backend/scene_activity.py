import clip
import torch
from PIL import Image
import torchvision.models as models
import torchvision.transforms as transforms
from config import Config

class SceneActivityRecognizer:
    def __init__(self):
        self.config = Config()
        self.clip_model, self.clip_preprocess = clip.load(self.config.CLIP_MODEL)
        self.places_model = models.__dict__['resnet50'](num_classes=365)
        checkpoint = torch.load(self.config.PLACES365_MODEL, map_location='cpu')
        self.places_model.load_state_dict(checkpoint['state_dict'])
        self.places_model.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    
    def get_scene_embedding(self, image_path: str):
        image = Image.open(image_path).convert('RGB')
        image = self.clip_preprocess(image).unsqueeze(0)
        with torch.no_grad():
            image_features = self.clip_model.encode_image(image)
        return image_features.squeeze(0).tolist()
    
    def get_place_category(self, image_path: str):
        image = Image.open(image_path).convert('RGB')
        image = self.transform(image).unsqueeze(0)
        with torch.no_grad():
            outputs = self.places_model(image)
        _, pred = outputs.topk(5, 1, True, True)
        return pred.tolist()[0]
    
    def detect_activity(self, image_path: str, activities: List[str]):
        image = Image.open(image_path).convert('RGB')
        image = self.clip_preprocess(image).unsqueeze(0)
        text = clip.tokenize(activities)
        
        with torch.no_grad():
            image_features = self.clip_model.encode_image(image)
            text_features = self.clip_model.encode_text(text)
            logits_per_image, _ = self.clip_model(image, text)
            probs = logits_per_image.softmax(dim=-1).squeeze(0).tolist()
        
        return dict(zip(activities, probs))