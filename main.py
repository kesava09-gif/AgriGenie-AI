import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image
from fpdf import FPDF
import tempfile
import pandas as pd
from streamlit_mic_recorder import mic_recorder
from deep_translator import GoogleTranslator
st.set_page_config(
    page_title="AgriGenie-AI",
    page_icon="🌱",
    layout="centered"
)

st.title("🌱 AgriGenie-AI")
st.subheader("AI Powered Smart Farming Assistant")

# ---------------- Gemini API ----------------

gemini_ready = False

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    gemini_ready = True
except:
    gemini_ready = False

# ---------------- Farmer Details ----------------

st.header("👨‍🌾 Farmer Details")

farmer = st.text_input("Farmer Name")
crop = st.text_input("Crop Name")
city = st.text_input("City")
if city:
    st.subheader("📍 Farmer Location")

    location = pd.DataFrame({
        "lat": [17.3850],
        "lon": [78.4867]
    })

    st.map(location)
soil = st.selectbox(
    "Select Soil Type",
    [
        "Black Soil",
        "Red Soil",
        "Clay Soil",
        "Sandy Soil"
    ]
)

st.divider()

# ---------------- Crop Recommendation ----------------

st.header("🌾 Crop Recommendation")

if st.button("Recommend Crop"):

    if soil == "Black Soil":
        st.success("Recommended Crop : Cotton")

    elif soil == "Red Soil":
        st.success("Recommended Crop : Groundnut")

    elif soil == "Clay Soil":
        st.success("Recommended Crop : Rice")

    else:
        st.success("Recommended Crop : Watermelon")

st.divider()

# ---------------- Weather ----------------

st.header("🌦 Weather Information")

if st.button("Get Weather"):

    if city == "":
        st.warning("Please enter city name")

    else:

        try:
            url = f"https://wttr.in/{city}?format=j1"

            data = requests.get(url).json()

            current = data["current_condition"][0]

            st.success("Weather Details")

            st.write(f"🌡 Temperature : {current['temp_C']} °C")
            st.write(f"💧 Humidity : {current['humidity']} %")
            st.write(f"☁ Condition : {current['weatherDesc'][0]['value']}")

        except:
            st.error("Unable to fetch weather")

st.divider()
st.divider()

st.header("💰 Crop Market Price")

if crop:

    crop_lower = crop.lower()

    if crop_lower == "rice":
        st.success("💰 Market Price: ₹2300 - ₹2600 / Quintal")

    elif crop_lower == "cotton":
        st.success("💰 Market Price: ₹7200 - ₹8200 / Quintal")

    elif crop_lower == "groundnut":
        st.success("💰 Market Price: ₹5800 - ₹7000 / Quintal")

    else:
        st.info("Market price not available.")

# ---------------- Fertilizer ----------------

st.header("🌱 Fertilizer Suggestion")

if crop:

    crop_lower = crop.lower()

    if crop_lower == "rice":
        st.info("Recommended Fertilizer : Urea")

    elif crop_lower == "cotton":
        st.info("Recommended Fertilizer : NPK 20-20-20")

    elif crop_lower == "groundnut":
        st.info("Recommended Fertilizer : Gypsum")

    else:
        st.info("Use organic compost and soil testing before applying fertilizers.")

st.divider()

# ---------------- Irrigation ----------------
st.divider()

# 👇 PASTE AI YIELD CODE HERE

st.header("🌾 AI Yield Prediction")

if crop:
    crop_lower = crop.lower()

    if crop_lower == "rice":
        st.success("🌾 Expected Yield: 25-35 Quintals / Acre")

    elif crop_lower == "cotton":
        st.success("🌾 Expected Yield: 8-12 Quintals / Acre")

    elif crop_lower == "groundnut":
        st.success("🌾 Expected Yield: 10-15 Quintals / Acre")

    else:
        st.info("Yield prediction not available.")

st.divider()

# ---------------- Irrigation ----------------

st.header("💧 Irrigation Tips")

if crop:

    if crop_lower == "rice":
        st.success("Keep field flooded with 2-5 cm water.")

    elif crop_lower == "cotton":
        st.success("Water every 7-10 days depending on weather.")

    elif crop_lower == "groundnut":
        st.success("Avoid excess watering during flowering.")

    else:
        st.success("Provide irrigation based on soil moisture.")

st.divider()

# ---------------- Plant Disease Detection ----------------

st.header("🌿 Plant Disease Detection")

leaf = st.file_uploader(
    "Upload Plant Leaf Image",
    type=["jpg", "jpeg", "png"]
)

if leaf:

    st.image(leaf, caption="Uploaded Leaf", use_container_width=True)

    if st.button("Detect Disease"):

        if not gemini_ready:
            st.error("Gemini API Key not configured.")

        else:
            image = Image.open(leaf)

            prompt = """
You are an agriculture expert.

Identify:
1. Plant name
2. Disease (if any)
3. Disease severity
4. Recommended pesticide
5. Organic treatment
6. Prevention tips

Give the answer in simple English.
"""

            try:
                response = model.generate_content([prompt, image])
                st.success(response.text)

            except Exception as e:
                st.error(f"Error: {e}")

st.divider()

# ---------------- AI Assistant ----------------

st.header("🤖 AI Farming Assistant")

question = st.text_area("Ask your farming question")
language = st.selectbox(
    "🌐 Select Language",
    ["English", "Telugu", "Hindi"]
)
audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    key="voice"
)

if audio:
    st.success("🎤 Voice recorded successfully!")
    st.info("Voice support added. Speech-to-text integration can be connected here.")

if st.button("Ask AI"):

    if not gemini_ready:
        st.error("Gemini API Key not configured.")

    elif question:

             try:
            response = model.generate_content(question)
            answer = response.text

            if language == "Telugu":
                answer = GoogleTranslator(source="auto", target="te").translate(answer)

            elif language == "Hindi":
                answer = GoogleTranslator(source="auto", target="hi").translate(answer)

            st.success(answer)

        except Exception as e:
            st.error(f"Error: {e}")

st.divider()

# ---------------- Summary ----------------

st.header("📋 Farm Summary")

if farmer and crop and city:

    st.success("Farmer Details Saved Successfully!")

    st.write(f"👨‍🌾 Farmer : {farmer}")
    st.write(f"🌾 Crop : {crop}")
    st.write(f"🏙️ City : {city}")
    st.write(f"🌍 Soil : {soil}")

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AgriGenie-AI Report", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Farmer: {farmer}", ln=True)
    pdf.cell(0, 10, f"Crop: {crop}", ln=True)
    pdf.cell(0, 10, f"City: {city}", ln=True)
    pdf.cell(0, 10, f"Soil: {soil}", ln=True)

    pdf_file = "AgriGenie_Report.pdf"
    pdf.output(pdf_file)

    with open(pdf_file, "rb") as f:
        st.download_button(
            "📄 Download Report",
            data=f,
            file_name="AgriGenie_Report.pdf",
            mime="application/pdf"
        )

st.divider()

st.caption("🌱 AgriGenie-AI Version 1.0")
st.caption("Developed by M. Kesavanath")
st.divider()
