---

# 🌱 **AgriSense AI**

### *AI-powered plant care, disease detection & farmer support — built for the fields of India.*

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/HuggingFace-Model-yellow?style=for-the-badge">
  <img src="https://img.shields.io/badge/Groq-LLM-green?style=for-the-badge">
</p>

<p align="center">
  <img src="https://github.com/your-banner-image.png" width="80%" alt="AgriSense Banner"/>  
</p>

---

## 🚀 **Overview**

**AgriSense AI** is a modern, farmer-centric platform that blends:

* 🌾 Computer vision
* 🌦️ Weather intelligence
* 🤖 Multilingual AI support
* 🏛️ Government scheme discovery
* 📞 Verified agriculture helplines

Designed specifically for **Indian farmers**, it simplifies plant care and provides actionable insights in seconds.

---

## 🌟 **Key Features**

### 🔍 **1. AI Disease Detection (Custom Model)**

Upload a leaf photo → instantly receive:

* Detected disease
* Confidence score
* Suggested treatment

Model is trained on curated datasets and deployed on **HuggingFace** for fast inference.

---

### 🌿 **2. Plant Species Identification**

Powered by **PlantNet API** → detects:

* Scientific name
* Common name
* Species confidence

---

### 🌦️ **3. Field Health Insights**

Real-time weather engine delivers:

* Temperature
* Humidity
* Rainfall
* Disease-favorability score
* 3-day outbreak risk prediction

---

### 🏛️ **4. Government Scheme Finder**

State-wise agriculture schemes such as:

* Subsidies
* Loans
* Soil health benefits
* Farmer insurance plans

Scraped & updated automatically.

---

### 🗣️ **5. AI Farming Assistant (Groq)**

Ask anything in your language:

* Irrigation tips
* Fertilizer schedule
* Disease treatment
* Climate-based recommendations

Uses ultra-fast **Groq LLM**.

---

### 🌐 **6. Multi-Language Support**

Includes:

* JSON-based UI translations
* Dynamic Groq LLM translation

---

### 📞 **7. Built-In Farmer Helplines**

* **Kisan Call Center:** *1800-180-1551*
* State-wise agriculture department contacts

---

## 🧠 **Architecture**

```
User Input
     ↓
Location API → Weather API → Scheme Scraper
     ↓                ↓                ↓
PlantNet API ← Image Upload → Disease Model
     ↓                ↓
         Processing Layer
 (Risk Engine · Insights Engine · AI Assistant)
     ↓
         Final Output to Farmer
(Plant ID · Disease · Forecast · Schemes · Helplines)
```

---

## 📁 **Project Structure**

```
📦 AgriSense-AI
├── app.py                     # Main Streamlit app
├── disease_model.py           # HuggingFace inference
├── plantnet_api.py            # Plant species identification
├── weather_api.py             # Weather + geocoding logic
├── scheme_scraper.py          # State-wise scheme extractor
├── translator.py              # Translation engine (JSON + LLM)
├── groq_assistant.py          # AI assistant logic
├── insights_engine.py         # Risk scoring + analysis
├── helplines.py               # Farmer helplines
├── i18n/                      # Static UI translations
└── requirements.txt
```

---

## 🔑 **API Keys Setup**

Create: **`.streamlit/secrets.toml`**

```toml
GROQ_API_KEY = "your-groq-key"
PLANTNET_API_KEY = "your-plantnet-key"
```

**How to get keys:**

| Service    | Link                                                             | Notes               |
| ---------- | ---------------------------------------------------------------- | ------------------- |
| Groq API   | [https://groq.com](https://groq.com)                             | Free tier available |
| PlantNet   | [https://my.plantnet.org/signup](https://my.plantnet.org/signup) | Required            |
| Open-Meteo | Free                                                             | No key required     |

---

## 🛠️ **Installation**

```bash
git clone https://github.com/prempatel-ai/codex.git
cd agrisense-ai
pip install -r requirements.txt
streamlit run app.py
```

📽️ Demo Video
<p align="center"> <a href="https://youtu.be/Mdw8fTINJLI" target="_blank"> <img src="https://img.youtube.com/vi/Mdw8fTINJLI/maxresdefault.jpg" alt="AgriSense AI Demo Video" width="75%" style="border-radius: 12px;"> </a> </p> <p align="center"> 🎥 **Click the thumbnail to watch the full demo on YouTube** </p>

---

## 🧬 **Model Notes**

The disease classifier is custom trained and deployed on **HuggingFace**.

Training pipeline includes:

* Dataset cleaning
* Data augmentation
* Transfer learning
* Validation & tuning
* Deployment as transformer-based classifier

Optimized for **common agricultural diseases** across India.

---

## 🤝 **Contributing**

We welcome contributions!
You can help by improving:

* Model accuracy
* Adding crops
* Adding regional languages
* UI/UX design
* Government scheme scraping

**Fork → Create Branch → Submit PR**

---

## ❤️ **Acknowledgements**

Built during the **Aviskaar Hackathon**
with the mission of making **AI accessible to every Indian farmer**.

---



