🌱 AgriSense AI
AI-powered plant care, disease detection & farmer support — built for the fields of India.
<p align="center"> <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge"> <img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge"> <img src="https://img.shields.io/badge/HuggingFace-Model-yellow?style=for-the-badge"> <img src="https://img.shields.io/badge/Groq-LLM-green?style=for-the-badge"> </p>
🚀 Overview

AgriSense AI is a modern, farmer-centered platform that combines computer vision, weather intelligence, AI-powered advice, and government support data into one simple, intuitive interface.

Designed for Indian farmers, AgriSense AI helps them:

Detect diseases early

Understand risk based on weather

Identify the plant species

Discover state government schemes

Access official 24×7 helplines

Get multilingual AI guidance

All features work seamlessly inside a clean, mobile-friendly Streamlit application.

🌟 Key Features
🔍 1. AI Disease Detection (Custom Trained Model)

We trained a plant disease classifier on curated images and deployed it on HuggingFace for fast inference.
Users upload a leaf photo → model outputs disease + confidence.

🌿 2. Plant Species Identification

Integrated with PlantNet API, enabling scientific name + common name identification.

🌦️ 3. Field Health Insights

Powered by real-time weather:

Temperature

Humidity

Rainfall

Disease-favorability score

3-day outbreak risk forecast

🏛️ 4. Government Scheme Finder

State-wise scheme scraper shows agriculture subsidies, loans, and benefits relevant to the farmer’s location.

🗣️ 5. AI Farming Assistant (Groq)

Farmers can ask anything—fertilizer schedule, treatment steps, irrigation advice—answered in simple language.

🌐 6. Multi-Language Support

Built using a dual system:

UI translations (JSON dictionary)

Dynamic translations via Groq LLM

📞 7. Official Helplines

Built-in:

Kisan Call Center (1800-180-1551)

State-wise agriculture helpline

🧠 Architecture
User Input
     ↓
Location API → Weather API → Scheme Scraper
     ↓                ↓               ↓
PlantNet API ← Image → Trained Disease Model
     ↓                ↓
           Processing Layer
    (Risk Engine · Insights Engine · LLM Advice)
     ↓
         Final Output to Farmer
(Plant ID · Disease · Forecast · Schemes · Helplines · Translations)

📁 Project Structure
📦 AgriSense-AI
├── app.py                     # Main Streamlit app
├── disease_model.py           # HuggingFace inference
├── plantnet_api.py            # Plant species identification
├── weather_api.py             # Weather + Geocoding logic
├── scheme_scraper.py          # State-wise scheme extractor
├── translator.py              # Translation engine (JSON + LLM)
├── groq_assistant.py          # AI assistant logic
├── insights_engine.py         # Risk scoring + analysis
├── helplines.py               # Official farmers’ helplines
├── i18n/                      # Static UI translations
└── requirements.txt

🔑 API Keys

Create .streamlit/secrets.toml:

GROQ_API_KEY = "your-groq-key"
PLANTNET_API_KEY = "your-plantnet-key"

How to get keys:

Groq API: https://groq.com

PlantNet API: https://my.plantnet.org/signup

Open-Meteo: Free, no key required

All keys stay hidden using Streamlit Secrets Manager.

🛠️ Installation
git clone https://github.com/your-username/agrisense-ai.git
cd agrisense-ai
pip install -r requirements.txt
streamlit run app.py

🧬 Model Notes

The disease model is custom trained and then deployed on HuggingFace for inference.
Training pipeline includes:

Image cleaning

Augmentation

Transfer learning

Validation & tuning

Deployment as transformer-based classifier

This ensures consistent, reliable predictions for common agricultural diseases.

🤝 Contributing

We welcome improvements!

Improve model accuracy

Add more crops

Add more languages

Enhance scheme scraping

UI/UX refinements

Fork → Create branch → Submit PR.

❤️ Acknowledgements

Built during a Aviskaar hackathon with the goal of making AI accessible to every Indian farmer.