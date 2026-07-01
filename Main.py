import streamlit as st
import google.generativeai as genai
import requests

st.set_page_config(
    page_title="AgriGenie-AI",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AgriGenie-AI")
st.subheader("AI Powered Smart Farming Assistant")

# Gemini API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    gemini_ready = True
except:
    gemini_ready = False

st.header("👨‍🌾 Farmer Details")

farmer = st.text_input("Farmer Name")

crop = st.text_input("Crop Name")

city = st.text_input("City")

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

st.header("🌾 Crop Recommendation")

if st.button("Recommend Crop"):

    if soil == "Black Soil":
        st.success("✅ Recommended Crop : Cotton")

    elif soil == "Red Soil":
        st.success("✅ Recommended Crop : Groundnut")

    elif soil == "Clay Soil":
        st.success("✅ Recommended Crop : Rice")

    else:
        st.success("✅ Recommended Crop : Watermelon")
