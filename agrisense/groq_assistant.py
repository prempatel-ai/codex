import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_comprehensive_analysis(plant_net_result, disease_result, location_info, weather_info):
    """
    Generates a comprehensive plant analysis using Groq LLM based on multiple inputs.

    Args:
        plant_net_result (dict): Result from PlantNet API (scientific_name, common_names, confidence).
        disease_result (dict): Result from Disease Detection Model (disease, confidence).
        location_info (str): User provided location string (e.g., "Mumbai, India").
        weather_info (dict): Weather data (temperature, humidity, rainfall).

    Returns:
        str: AI-generated analysis and advice.
    """
    if not GROQ_API_KEY:
        return "⚠️ Groq API Key is missing. Please add it to the .env file."

    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        # Constructing the prompt
        prompt = f"""
        You are an expert agricultural botanist and plant pathologist. 
        Analyze the following plant data and provide a comprehensive report.

        ### 1. Input Data
        
        **📍 Location & Environment:**
        - Location: {location_info}
        - Current Weather: {weather_info.get('temperature', 'N/A')}°C, Humidity: {weather_info.get('humidity', 'N/A')}%, Rainfall: {weather_info.get('rainfall', 'N/A')}mm
        
        **🌿 Plant Identification (from PlantNet):**
        """
        
        if plant_net_result:
            prompt += f"""
            - Scientific Name: {plant_net_result.get('scientific_name')}
            - Common Names: {', '.join(plant_net_result.get('common_names', []))}
            - Identification Confidence: {plant_net_result.get('confidence', 0) * 100:.1f}%
            """
        else:
            prompt += "\n- Plant Identification failed or not available.\n"

        prompt += f"""
        **🦠 Disease Detection (from AI Model):**
        - Detected Condition: {disease_result.get('disease')}
        - Confidence: {disease_result.get('confidence', 0) * 100:.1f}%
        """

        prompt += """
        ### 2. Required Output Format
        
        Please provide a structured response in Markdown with the following sections:

        **1. 🌿 Plant Description**
        - Briefly describe the identified plant (if known).
        - Mention its typical characteristics and uses.

        **2. 🩺 Health Evaluation**
        - Analyze the detected disease/condition: {disease_result.get('disease')}.
        - Is this a serious threat? What are the visible symptoms usually associated with it?
        - How does the current weather ({weather_info.get('temperature')}°C, {weather_info.get('humidity')}%) impact this disease?

        **3. 🛡️ Treatment & Care Suggestions**
        - **Immediate Actions:** What should the user do right now?
        - **Preventive Measures:** How to stop it from spreading?
        - **Long-term Care:** Watering, soil, and sunlight requirements adapted to the current location/weather.

        **4. 💡 Additional Insights**
        - Any specific tips for growing this plant in {location_info}?
        
        Keep the tone helpful, professional, and easy for a farmer or gardener to understand.
        """
        
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are AgriSense AI, a helpful and knowledgeable agricultural assistant."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_tokens=1024,
        )
        
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"❌ Error generating analysis: {str(e)}"
