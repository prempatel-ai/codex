import streamlit as st
from PIL import Image
import io
import os
import json
import translator

# Import backend modules
import weather_api
import plantnet_api
import disease_model
import groq_assistant
import risk_engine
import advice_engine

import field_insights
import scheme_scraper
import indian_locations
import helplines

# Load UI Text
try:
    with open("i18n/ui_text.json", "r", encoding="utf-8") as f:
        ui_text = json.load(f)
except Exception as e:
    print(f"Error loading UI text: {e}")
    ui_text = {} # Fallback

# Page Config
st.set_page_config(
    page_title="AgriSense AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    h1 {
        color: #1b5e20;
    }
    h2, h3 {
        color: #2e7d32;
    }
    .risk-high {
        background-color: #ffebee;
        color: #b71c1c;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #c62828;
    }
    .risk-medium {
        background-color: #fff3e0;
        color: #e65100;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ef6c00;
    }
    .risk-low {
        background-color: #e8f5e9;
        color: #1b5e20;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #2e7d32;
    }
    .field-insights-box {
        background-color: #ffffff;
        color: #000000;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .field-insights-box p, .field-insights-box h4, .field-insights-box li {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper to get text safely
def get_text(key):
    lang = st.session_state.get("language", "English")
    return ui_text.get(lang, {}).get(key, ui_text.get("English", {}).get(key, key))

# Header & Language Selector
col_header, col_lang = st.columns([8, 2])

with col_lang:
    selected_language = st.selectbox(
        "🌐 Language", 
        ["English", "Hindi", "Marathi", "Tamil", "Telugu", "Gujarati", "Kannada", "Punjabi", "Bengali", "Odia", "Malayalam"],
        index=0,
        key="language_selector" # Added a key to prevent potential issues with multiple selectboxes
    )
    st.session_state["language"] = selected_language

with col_header:
    st.title(f"🌱 {get_text('app_title')}")
    st.markdown(f"### {get_text('app_subtitle')}")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/tractor.png", width=100)
    st.title(get_text('app_title'))
    st.info(get_text('app_tagline')) # Changed from app_subtitle to app_tagline for sidebar
    
    st.markdown("---")
    st.markdown(f"### 👨‍🌾 {get_text('sidebar_credits')}")
    st.markdown(get_text('sidebar_credits_text'))
    st.markdown(f"[{get_text('github_repo')}]({get_text('github_repo_link')})")
    
    st.markdown("---")
    st.markdown(f"### ℹ️ {get_text('sidebar_how_to')}")
    st.markdown(get_text('sidebar_how_to_steps'))
    
    st.markdown("---")
    st.markdown("### 📞 24×7 Farmer Support Helplines")
    st.markdown("**🇮🇳 Kisan Call Center (24×7)**  \n📞 1800-180-1551  \n🗣️ Support in 22 Indian languages")
    
    state = st.session_state.get("state_name")
    if state:
        helpline = helplines.get_state_helpline(state)
        if helpline:
            st.markdown("---")
            st.markdown(f"### 🌾 State Agriculture Helpline")
            st.markdown(f"**State:** {state}  \n**📞 Contact:** {helpline}")

# Main Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(get_text('section_a'))
    
    # Modern Auto-suggest Search (Restricted to India)
    selected_loc_input = st.selectbox(
        get_text('search_label'),
        options=[get_text('select_location_placeholder')] + indian_locations.INDIAN_LOCATIONS,
        index=0,
        help=get_text('search_help')
    )
    
    # Check if a valid location is selected (not the placeholder)
    if selected_loc_input and selected_loc_input != get_text('select_location_placeholder'):
        # Only trigger if the selection has changed to avoid loops, 
        # though st.selectbox handles state well.
        # We want to fetch weather automatically when this changes.
        
        # Check if we need to update
        current_selection = st.session_state.get("selected_location", "")
        
        # If the user selected a new location, or if we haven't fetched weather for it yet
        if selected_loc_input != current_selection:
            st.session_state['selected_location'] = selected_loc_input
            
            # Extract state name for schemes
            # Format is usually "City, State" or just "State"
            if "," in selected_loc_input:
                st.session_state['state_name'] = selected_loc_input.split(",")[-1].strip()
            else:
                st.session_state['state_name'] = selected_loc_input
            
            with st.spinner(get_text('fetch_weather_spinner').format(location=selected_loc_input)):
                # Pass the selected location directly. weather_api will filter for India.
                query_for_api = selected_loc_input
                    
                lat, lon = weather_api.get_coordinates(query_for_api)
                
                if lat and lon:
                    weather_data = weather_api.get_weather(lat, lon)
                    if weather_data:
                        st.success(get_text('weather_fetch_success').format(location=selected_loc_input))
                        st.session_state['weather_data'] = weather_data
                        
                        # Fetch Schemes
                        if 'state_name' in st.session_state:
                            with st.spinner(get_text('schemes_spinner').format(state=st.session_state['state_name'])):
                                schemes = scheme_scraper.scrape_schemes_by_state(st.session_state['state_name'])
                                st.session_state['schemes'] = schemes
                        
                        st.rerun()
                    else:
                        st.error(get_text('weather_fetch_error'))
                else:
                    st.error(get_text('coordinates_error'))

    # Display Weather if available
    if 'weather_data' in st.session_state:
        wd = st.session_state['weather_data']
        lang = st.session_state.get("language", "English")
        
        selected_loc_display = st.session_state.get('selected_location', get_text('unknown'))
        if lang != "English":
            selected_loc_display = translator.translate_dynamic_text(selected_loc_display, lang)

        st.info(f"🌍 {get_text('selected_location_label')}: **{selected_loc_display}**")
        st.info(f"🌡️ {get_text('temperature_label')}: {wd['temperature']}°C | 💧 {get_text('humidity_label')}: {wd['humidity']}% | 🌧️ {get_text('rainfall_label')}: {wd['rainfall']}mm")

    st.subheader(get_text('section_b'))
    
    if 'weather_data' in st.session_state:
        wd = st.session_state['weather_data']
        lang = st.session_state.get("language", "English")
        
        # Calculate Insights
        suitability_score, suitability_cat = field_insights.compute_environmental_suitability(
            wd['temperature'], wd['humidity'], wd['rainfall']
        )
        
        warning_text, warning_level = field_insights.outbreak_warning(
            wd['temperature'], wd['humidity'], wd['rainfall']
        )
        
        mon_rec = field_insights.monitoring_recommendation(warning_level)
        
        summary_text = field_insights.field_summary(
            wd['temperature'], wd['humidity'], wd['rainfall']
        )
        
        # Translate Dynamic Content
        if lang != "English":
            suitability_cat = translator.translate_dynamic_text(suitability_cat, lang)
            warning_text = translator.translate_dynamic_text(warning_text, lang)
            mon_rec = translator.translate_dynamic_text(mon_rec, lang)
            summary_text = translator.translate_dynamic_text(summary_text, lang)

        # Display Insights
        st.markdown(f"""
        <div class="field-insights-box">
            <p style="color:black;"><strong>{get_text('suitability_score_label')}:</strong> {suitability_score}/100 ({suitability_cat})</p>
            <progress value="{suitability_score}" max="100" style="width:100%"></progress>
            <br><br>
            <p style="color:black;"><strong>{get_text('outbreak_warning_label')}:</strong><br>{warning_text}</p>
            <p style="color:black;"><strong>{get_text('monitoring_label')}:</strong> {mon_rec}</p>
            <hr>
            <p style="color:black;"><em>{summary_text}</em></p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.info(get_text('fetch_weather_for_insights'))


with col2:
    st.subheader(get_text('section_c'))
    uploaded_file = st.file_uploader(get_text('upload_label'), type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption=get_text('uploaded_image_caption'), width=300)
        
        # Convert image to bytes for PlantNet
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format)
        img_bytes = img_byte_arr.getvalue()
        
        # Run Analysis
        if st.button(get_text('analyze_button')):
            with st.spinner(get_text('analyzing_spinner')):
                # 1. Disease Detection
                disease_result = disease_model.predict_disease(image)
                st.session_state['disease_result'] = disease_result
                
                # 2. Plant Identification (Updated Logic)
                # Save temp file for PlantNet API
                temp_image_path = "temp_plant_image.jpg"
                with open(temp_image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                plantnet_api_key = os.getenv("PLANTNET_API_KEY")
                plant_id_result = plantnet_api.identify_plant_with_plantnet(temp_image_path, plantnet_api_key)
                st.session_state['plant_id_result'] = plant_id_result
                
                # Clean up temp file (optional, but good practice)
                if os.path.exists(temp_image_path):
                    os.remove(temp_image_path)

# Results Section
if 'disease_result' in st.session_state and st.session_state['disease_result']:
    st.markdown("---")
    res_col1, res_col2 = st.columns(2)
    
    disease_res = st.session_state['disease_result']
    plant_res = st.session_state.get('plant_id_result')
    weather_res = st.session_state.get('weather_data')
    lang = st.session_state.get("language", "English")
    
    with res_col1:
        st.subheader(get_text('section_d'))
        
        d_name = disease_res['disease']
        if lang != "English":
            d_name = translator.translate_dynamic_text(d_name, lang)
            
        st.metric(get_text('detected_disease'), d_name)
        st.metric(get_text('confidence'), f"{disease_res['confidence']*100:.2f}%")
        
        risk_score = 0
        risk_level = "Unknown"
        if weather_res:
            risk_data = risk_engine.calculate_risk(
                weather_res['humidity'],
                weather_res['rainfall'],
                weather_res['temperature'],
                disease_res['confidence']
            )
            risk_score = risk_data['score']
            risk_level = risk_data['level']
            
            risk_level_display = risk_level
            if lang != "English":
                risk_level_display = translator.translate_dynamic_text(risk_level, lang)
            
            st.subheader(get_text('risk_analysis'))
            risk_class = f"risk-{risk_level.lower()}" # Use original English level for CSS class
            st.markdown(f"""
            <div class="{risk_class}">
                <h4>{get_text('risk_level')}: {risk_level_display}</h4>
                <p>{get_text('risk_score')}: {risk_score}/100</p>
            </div>
            """, unsafe_allow_html=True)
            
    with res_col2:
        st.subheader(get_text('section_e'))
        if plant_res:
            st.markdown(f"### 🌿 {get_text('plant_id_result')}")
            
            sci_name = plant_res['scientific_name']
            common_names = ', '.join(plant_res['common_names'])
            
            if lang != "English":
                # Scientific names usually stay Latin, but common names can be translated
                common_names = translator.translate_dynamic_text(common_names, lang)
            
            st.write(f"**{get_text('scientific_name')}:** *{sci_name}*")
            st.write(f"**{get_text('common_names')}:** {common_names}")
            st.write(f"**{get_text('confidence')}:** {plant_res['confidence']*100:.2f}%")
        else:
            st.warning(get_text('plantnet_error'))

    # Section H: Government Schemes
    st.markdown("---")
    state_name = st.session_state.get('state_name', get_text('your_state'))
    
    # Translate state name for header if needed, but usually proper nouns stay
    state_name_display = state_name
    if lang != "English":
        state_name_display = translator.translate_dynamic_text(state_name, lang)
        
    st.subheader(f"{get_text('section_h')} {state_name_display}")
    
    selected_loc = st.session_state.get('selected_location', '')
    country_name = "India" # Default
    if "," in selected_loc:
        country_name = selected_loc.split(",")[-1].strip()
        
    if country_name.lower() != "india":
        st.info(get_text('schemes_country_warning').format(country=country_name))
    elif 'schemes' in st.session_state and st.session_state['schemes']:
        for scheme in st.session_state['schemes']:
            title = scheme['title']
            desc = scheme['description']
            benefits = scheme['benefits']
            eligibility = scheme['eligibility']
            how_to = scheme['how_to_apply']
            
            if lang != "English":
                title = translator.translate_dynamic_text(title, lang)
                desc = translator.translate_dynamic_text(desc, lang)
                benefits = translator.translate_dynamic_text(benefits, lang)
                eligibility = translator.translate_dynamic_text(eligibility, lang)
                how_to = translator.translate_dynamic_text(how_to, lang)

            with st.expander(f"🟩 {title}"):
                st.markdown(f"**{get_text('description_label')}:** {desc}")
                st.markdown(f"**{get_text('benefits_label')}:** {benefits}")
                st.markdown(f"**{get_text('eligibility_label')}:** {eligibility}")
                st.markdown(f"**{get_text('how_to_apply_label')}:** {how_to}")
                st.markdown(f"🔗 [{get_text('official_link')}]({scheme['official_link']})")
    elif 'state_name' in st.session_state:
        st.warning(get_text('no_schemes'))
    else:
        st.info(get_text('select_location_msg'))

    # Advice Section
    st.markdown("---")
    st.subheader(get_text('section_g'))
    
    advice = advice_engine.get_treatment_advice(disease_res['disease'])
    if lang != "English":
        advice = translator.translate_dynamic_text(advice, lang)
        
    st.info(f"💡 **{get_text('recommendation')}:** {advice}")

    # Groq Assistant
    st.markdown("---")
    st.subheader(get_text('section_f'))
    
    if st.button(get_text('ask_ai_button')):
        if not weather_res:
            st.warning(get_text('weather_data_required_warning'))
        else:
            with st.spinner(get_text('consulting_ai_spinner')):
                # Prepare inputs
                location_info = st.session_state.get('selected_location', get_text('unknown_location'))
                
                ai_response = groq_assistant.generate_comprehensive_analysis(
                    plant_net_result=plant_res,
                    disease_result=disease_res,
                    location_info=location_info,
                    weather_info=weather_res
                )
                
                if lang != "English":
                    ai_response = translator.translate_dynamic_text(ai_response, lang)
                    
                st.markdown(ai_response)
