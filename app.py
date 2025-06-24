import streamlit as st
import requests
import numpy as np
import pickle
from datetime import datetime

# Title
st.title("🌤️ Live Climate Prediction App")
st.write("Enter your city to fetch current weather and predict temperature using ML model.")

# Input
city = st.text_input("Enter City Name")

# Load trained model (model.pkl must be present in same folder)
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("❌ Model file 'model.pkl' not found. Please upload it.")
    st.stop()

# API Key - Replace this with your actual key
API_KEY = "59ee022209c951f6e890fcb003601894"

def get_weather(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return None, data.get("message", "Unknown error")

    weather_data = {
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "hour": datetime.now().hour
    }
    return weather_data, None

# Prediction Button
if st.button("Get Climate Prediction"):
    weather, error = get_weather(city)

    if weather:
        st.subheader(f"🌐 Live Weather Data for {city}")
        st.write(f"Humidity: {weather['humidity']}%")
        st.write(f"Pressure: {weather['pressure']} hPa")
        st.write(f"Wind Speed: {weather['wind_speed']} m/s")
        st.write(f"Hour of Day: {weather['hour']}")

        # Prepare input for model
        input_features = np.array([[weather["humidity"], weather["pressure"], weather["wind_speed"], weather["hour"]]])
        try:
            predicted_temp = model.predict(input_features)[0]
            st.success(f"🌡️ Predicted Temperature: {predicted_temp:.2f}°C")
        except Exception as e:
            st.error(f"Prediction error: {e}")

        st.info(f"📡 Actual Temperature Now: {weather['temp']}°C")
    else:
        st.error(f"Failed to fetch weather data: {error}")
