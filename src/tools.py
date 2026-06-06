import os
import requests
from crewai.tools import tool

@tool("Weather Tool")
def get_weather(city: str) -> str:
    """Gets the current real-time weather for a given city. Use this to check
      the actual weather before suggesting outdoor activities or what to pack."""

    api_key = os.getenv("WEATHER_API_KEY")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",   # metric = Celsius
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return f"Could not get weather for {city} (error {response.status_code})."

    data = response.json()
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    return f"The weather in {city} is currently {temp}°C with {description}."