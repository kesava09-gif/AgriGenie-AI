import streamlit as st
import google.generativeai as genai
import os

# Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(
    page_title="AgriGenie-AI",
    page_icon="🌱"
)

st.title("🌱 AgriGenie-AI")
st.write("AI Powered Smart Farming Assistant")

farmer = st.text_input("👨‍🌾 Farmer Name")
crop = st.text_input("🌾 Crop Name")
city = st.text_input("🏙️ City")

soil = st.selectbox(
    "🌍 Select Soil Type",
    ["Black Soil", "Red Soil", "Clay Soil", "Sandy Soil"]
)

if st.button("🌱 Recommend Crop"):

    if soil == "Black Soil":
        st.success("Recommended Crop: Cotton")

    elif soil == "Red Soil":
        st.success("Recommended Crop: Groundnut")

    elif soil == "Clay Soil":
        st.success("Recommended Crop: Rice")

    else:
        st.success("Recommended Crop: Watermelon")

st.divider()

st.header("🤖 AI Farming Assistant")

question = st.text_area("Ask your farming question")

if st.button("Ask AI"):
    if question:
        try:
            response = model.generate_content(question)
            st.success(response.text)
        except Exception:
            st.error("Gemini API Key not configured. Add your GEMINI_API_KEY in Environment Variables.")
