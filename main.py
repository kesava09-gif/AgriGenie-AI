import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image
from fpdf import FPDF
import tempfile
import pandas as pd

# ------------------ Page Config ------------------

st.set_page_config(
    page_title="AgriGenie-AI",
    page_icon="🌱",
    layout="centered"
)

st.title("🌱 AgriGenie-AI")
st.subheader("AI Powered Smart Farming Assistant")

# ------------------ Gemini API ------------------

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

# ------------------ Farmer Details ------------------

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
