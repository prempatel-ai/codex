def calculate_risk(humidity, rainfall, temperature, disease_confidence):
    """
    Calculates risk score based on environmental factors and disease confidence.
    
    Rules:
    risk = disease_confidence * 100 (if confidence is 0-1)
    if humidity > 70: risk += 10
    if rainfall > 2: risk += 10
    if 20 <= temperature <= 30: risk += 10
    if risk > 100: risk = 100
    """
    # Base risk from disease confidence (assuming confidence is 0.0 to 1.0)
    risk = disease_confidence * 100
    
    if humidity is not None and humidity > 70:
        risk += 10
        
    if rainfall is not None and rainfall > 2:
        risk += 10
        
    if temperature is not None and 20 <= temperature <= 30:
        risk += 10
        
    # Cap risk at 100
    risk = min(risk, 100)
    
    # Determine level
    if risk < 50:
        level = "Low"
    elif 50 <= risk <= 75:
        level = "Medium"
    else:
        level = "High"
        
    return {
        "score": round(risk, 2),
        "level": level
    }
