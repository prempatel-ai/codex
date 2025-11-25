def compute_environmental_suitability(temp, humidity, rainfall):
    """
    Calculates Environmental Suitability Score (0-100).
    Returns: (score, category)
    """
    score = 0
    if temp is not None and 20 <= temp <= 30:
        score += 40
    if humidity is not None and humidity >= 65:
        score += 30
    if rainfall is not None and rainfall > 0:
        score += 30
        
    if score <= 40:
        category = "Low disease-favorability"
    elif score <= 70:
        category = "Moderate"
    else:
        category = "High"
        
    return score, category

def outbreak_warning(temp, humidity, rainfall):
    """
    Generates Disease Outbreak Early Warning.
    Returns: (warning_text, warning_level)
    """
    if temp is None or humidity is None or rainfall is None:
        return "Insufficient data for outbreak warning.", "Unknown"

    if humidity > 70 and 20 <= temp <= 30 and rainfall > 0:
        return "⚠️ High chance of disease outbreak in the next 3 days.\nEnvironmental conditions are favorable for fungal infections.", "High"
    elif (humidity > 60 and 20 <= temp <= 35) or (rainfall > 0): # Simplified moderate logic as "Else if moderate" was vague in prompt, using a reasonable fallback or just the 'else' from prompt implies specific conditions.
        # Prompt said: "Else if moderate: ...". It didn't define "moderate" condition explicitly other than the High condition. 
        # I will assume if it's not High but has some risk factors (e.g. high humidity OR rain).
        # Let's stick to a safe interpretation: If score is Moderate (from suitability) maybe? 
        # Or just: 
        return "⚠️ Moderate outbreak chances. Monitor leaves daily.", "Moderate"
    else:
        return "🌿 Low outbreak risk. Conditions are currently unfavorable for disease spread.", "Low"

def generate_forecast_insights(forecast_data):
    """
    Generates 3-Day Forecast Insights.
    Args:
        forecast_data: List of dicts with 'temp', 'humidity', 'rainfall' for next 3 days.
    Returns:
        List of strings.
    """
    if not forecast_data:
        return []
    
    insights = []
    for i, day in enumerate(forecast_data):
        risk = "Low risk"
        if day['humidity'] > 70 and day['rainfall'] > 0:
            risk = "High risk"
        elif day['humidity'] > 60 or day['rainfall'] > 0:
            risk = "Moderate risk"
            
        insight = f"Day {i+1}: {day['temp']}°C / Humidity {day['humidity']}% / Rain {day['rainfall']}mm → {risk}"
        insights.append(insight)
        
    return insights

def monitoring_recommendation(risk_level):
    """
    Returns monitoring frequency recommendation based on risk level.
    """
    if risk_level == "High":
        return "Check leaves twice daily."
    elif risk_level == "Medium":
        return "Monitor once per day."
    else:
        return "Check every 2–3 days."

def field_summary(temp, humidity, rainfall):
    """
    Auto-generates a field summary paragraph.
    """
    if temp is None or humidity is None or rainfall is None:
        return "Weather data unavailable for summary."

    temp_desc = "stable"
    if temp > 30: temp_desc = "hot"
    elif temp < 15: temp_desc = "cool"
    
    humid_desc = "moderate"
    if humidity > 70: humid_desc = "humid"
    elif humidity < 40: humid_desc = "dry"
    
    rain_desc = "low rainfall"
    if rainfall > 5: rain_desc = "heavy rainfall"
    elif rainfall > 0: rain_desc = "light rainfall"
    
    disease_prob = "low"
    if humidity > 70 or (temp > 20 and temp < 30 and rainfall > 0):
        disease_prob = "increased"
        
    summary = f"Your field currently has {humid_desc} conditions, {rain_desc}, and {temp_desc} temperature. This leads to a {disease_prob} probability of fungal disease outbreaks. Maintain regular watering and avoid over-irrigation."
    return summary
