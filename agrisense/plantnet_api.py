import requests
import os
import json

def identify_plant_with_plantnet(image_file_path, api_key):
    """
    Identifies a plant using the PlantNet API with a specific file upload format.
    
    Args:
        image_file_path (str): Path to the image file.
        api_key (str): PlantNet API key.
        
    Returns:
        dict: Parsed result with scientific name, common names, and confidence, or None if failed.
    """
    if not api_key:
        return None

    api_url = f"https://my-api.plantnet.org/v2/identify/all?api-key={api_key}"
    
    try:
        # Use the exact format requested
        files = [
            ('images', (image_file_path, open(image_file_path, 'rb'), 'image/jpeg'))
        ]
        payload = {}

        response = requests.post(api_url, files=files, data=payload)

        if response.status_code != 200:
            return None

        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            best_match = data["results"][0]
            species = best_match["species"]
            common_names = species.get("commonNames", [])
            
            return {
                "scientific_name": species["scientificNameWithoutAuthor"],
                "common_names": common_names,
                "confidence": best_match["score"]
            }
        
        return None
        
    except Exception as e:
        print(f"Error in PlantNet API: {e}")
        return None
