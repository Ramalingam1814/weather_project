import streamlit as st
import requests
import numpy as np
from datetime import datetime
import pickle

# Title
st.title("🌤️ Live Climate Prediction App")
st.write("Enter your city to fetch current weather and predict temperature using ML model.")

# Input
city = st.text_input("Enter City Name", "Chennai")

# Load ML model (make sure you have the trained .pkl file)
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("ML model file not found. Please train and save 'weather_model.pkl' first.")
    st.stop()

# Define your API Key
API_KEY = "59ee022209c951f6e890fcb003601894"  # 🔴 Replace with your OpenWeatherMap API key

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

# Button to trigger prediction
if st.button("Get Climate Prediction"):
    weather, error = get_weather(city)

    if weather:
        # Show live values
        st.subheader(f"🌐 Live Weather Data for {city}")
        st.write(f"Humidity: {weather['humidity']}%")
        st.write(f"Pressure: {weather['pressure']} hPa")
        st.write(f"Wind Speed: {weather['wind_speed']} m/s")
        st.write(f"Hour: {weather['hour']}")

        # Predict temperature
        features = np.array([[weather["humidity"], weather["pressure"], weather["wind_speed"], weather["hour"]]])
        predicted_temp = model.predict(features)[0]

        st.success(f"🌡️ Predicted Temperature: {predicted_temp:.2f}°C")
        st.info(f"📡 Actual Temperature: {weather['temp']}°C")
    else:
        st.error(f"Failed to fetch weather data: {error}")
