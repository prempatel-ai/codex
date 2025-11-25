# 🌱 AgriSense AI

AgriSense AI is a smart crop disease detector and assistant powered by Artificial Intelligence. It helps farmers and agricultural enthusiasts identify plant diseases, get weather-based risk analysis, and receive expert advice.

## Features

- **Crop Disease Detection**: Uses a HuggingFace Transformer model to detect diseases from leaf images.
- **Plant Identification**: Identifies plant species using the PlantNet API.
- **Weather Integration**: Fetches real-time weather data (Temperature, Humidity, Rainfall) using Open-Meteo API.
- **Risk Analysis**: Calculates disease risk based on environmental factors and disease confidence.
- **AI Assistant**: "Know Your Plant" feature powered by Groq LLM to answer specific queries about the crop.
- **Treatment Advice**: Provides actionable advice for detected diseases.

## Setup & Installation

1.  **Clone the repository** (or ensure you have the project files).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure API Keys**:
    - Open `.env` file.
    - Add your Groq API Key: `GROQ_API_KEY=your_key_here`.
    - (Optional) Update PlantNet API Key if needed.

## How to Run

Run the Streamlit application:

```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application.
- `disease_model.py`: Handles disease detection logic.
- `plantnet_api.py`: Handles plant identification via PlantNet.
- `weather_api.py`: Fetches weather data.
- `groq_assistant.py`: AI Assistant logic.
- `risk_engine.py`: Calculates risk scores.
- `advice_engine.py`: Provides treatment advice.
- `requirements.txt`: List of dependencies.

## Credits

Built with ❤️ by the AgriSense Team.
