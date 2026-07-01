import streamlit as st
import google.generativeai as genai
import requests

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
st.header("🌿 Plant Disease Detection")

leaf = st.file_uploader(
    "Upload Plant Leaf Image",
    type=["jpg", "jpeg", "png"]
)

if leaf:
    st.image(leaf, caption="Uploaded Leaf", use_container_width=True)

    if st.button("Detect Disease"):
        st.info("🚧 Disease Detection module coming soon...")
# ---------------- AI Assistant ----------------

st.header("🤖 AI Farming Assistant")

question = st.text_area("Ask your farming question")

if st.button("Ask AI"):

    if not gemini_ready:
        st.error("Gemini API Key not configured.")

    elif question:

        try:
            response = model.generate_content(question)
            st.success(response.text)

        except Exception as e:
            st.error(f"Error : {e}")

st.divider()

# ---------------- Summary ----------------

st.header("📋 Farm Summary")

if farmer and crop and city:

    st.success("Farmer Details Saved Successfully!")

    st.write("### Summary")
    st.write(f"👨‍🌾 Farmer : {farmer}")
    st.write(f"🌾 Crop : {crop}")
    st.write(f"🏙 City : {city}")
    st.write(f"🌍 Soil : {soil}")

st.divider()

st.caption("🌱 AgriGenie-AI Version 1.0")
st.caption("Developed by M. Kesavanath")
