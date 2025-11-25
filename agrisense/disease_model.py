from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
from PIL import Image

# Cache model and processor to avoid reloading on every prediction
_model = None
_processor = None

def load_model():
    """
    Loads the HuggingFace model and processor.
    """
    global _model, _processor
    if _model is None or _processor is None:
        try:
            model_name = "Diginsa/Plant-Disease-Detection-Project"
            _processor = AutoImageProcessor.from_pretrained(model_name)
            _model = AutoModelForImageClassification.from_pretrained(model_name)
        except Exception as e:
            print(f"Error loading model: {e}")
            return None, None
    return _model, _processor

def predict_disease(image):
    """
    Predicts disease from a leaf image.
    Args:
        image: PIL Image object
    Returns:
        dict: { "disease": str, "confidence": float }
    """
    model, processor = load_model()
    if model is None or processor is None:
        return None

    try:
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_class_idx = logits.argmax(-1).item()
            confidence = torch.softmax(logits, dim=-1).max().item()
            
        disease_name = model.config.id2label[predicted_class_idx]
        
        return {
            "disease": disease_name,
            "confidence": confidence
        }
    except Exception as e:
        print(f"Error predicting disease: {e}")
        return None
