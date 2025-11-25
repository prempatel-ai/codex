import requests

def get_coordinates(location_name):
    """
    Fetches latitude and longitude for a given location name using Open-Meteo Geocoding API.
    """
    try:
        # Fetch more results to filter for India
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={location_name}&count=10&language=en&format=json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # If no results and comma exists, try searching for the first part (City)
        if "results" not in data or len(data["results"]) == 0:
            if "," in location_name:
                city_only = location_name.split(",")[0].strip()
                url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_only}&count=10&language=en&format=json"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

        if "results" in data and len(data["results"]) > 0:
            # Filter for India
            for result in data["results"]:
                if result.get("country_code") == "IN" or result.get("country") == "India":
                    return result["latitude"], result["longitude"]
            
            # Fallback: Return first result if no India match found
            result = data["results"][0]
            return result["latitude"], result["longitude"]
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None, None

def geocode_suggestions(query):
    """
    Fetches location suggestions for a query string.
    Returns a list of dicts with name, admin1, country, lat, lon.
    """
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=10&language=en&format=json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        suggestions = []
        if "results" in data:
            for result in data["results"]:
                suggestions.append({
                    "id": result.get("id"),
                    "name": result.get("name"),
                    "admin1": result.get("admin1", ""),
                    "country": result.get("country", ""),
                    "latitude": result.get("latitude"),
                    "longitude": result.get("longitude")
                })
        return suggestions
    except Exception as e:
        print(f"Error fetching suggestions: {e}")
        return []

def get_weather(lat, lon):
    """
    Fetches current weather data (temperature, humidity, rainfall) for given coordinates using Open-Meteo Forecast API.
    """
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if "current" in data:
            current = data["current"]
            return {
                "temperature": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "rainfall": current.get("precipitation")
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None
