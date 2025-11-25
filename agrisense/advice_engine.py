def get_treatment_advice(disease_name):
    """
    Returns treatment advice based on the detected disease.
    """
    advice_db = {
        "Early Blight": "Remove infected leaves, avoid overhead irrigation, use recommended fungicide.",
        "Late Blight": "Improve drainage, use copper-based fungicides, monitor daily.",
        "Healthy": "Your plant looks healthy. Continue normal care.",
        "Powdery Mildew": "Prune for air circulation, use sulfur-based fungicides, avoid nitrogen fertilizer.",
        "Leaf Spot": "Remove affected leaves, avoid wetting foliage, apply copper fungicide.",
        "Rust": "Remove infected parts, avoid overhead watering, apply sulfur or copper fungicides.",
        "Bacterial Spot": "Use copper sprays, avoid overhead irrigation, remove infected debris.",
        "Mosaic Virus": "Remove and destroy infected plants, control aphids, sanitize tools.",
        "Yellow Leaf Curl Virus": "Control whiteflies, use resistant varieties, remove infected plants.",
        "Spider Mites": "Use insecticidal soap or neem oil, increase humidity.",
        "Target Spot": "Improve air circulation, use fungicides if severe.",
        "Septoria Leaf Spot": "Remove lower leaves, apply fungicide, rotate crops."
    }
    
    # Default advice if disease not in DB
    default_advice = "Consult a local agricultural expert for specific treatment options."
    
    # Simple partial match or exact match
    for key in advice_db:
        if key.lower() in disease_name.lower():
            return advice_db[key]
            
    return default_advice
