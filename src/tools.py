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


@tool("Web Search Tool")
def search_web(query: str) -> str:
    """Searches the web for current, real-world information. Use this to find
    up-to-date facts — like real hotel names and prices, restaurants,
    attractions, or transport options — instead of guessing from memory."""

    api_key = os.getenv("SERPER_API_KEY")
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }
    payload = {"q": query}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Could not search the web (error {response.status_code})."

    data = response.json()
    results = data.get("organic", [])   # the list of search results

    if not results:
        return f"No web results found for '{query}'."

    # take the top 5 results and turn each into a readable line
    lines = []
    for item in results[:5]:
        title   = item.get("title", "")
        snippet = item.get("snippet", "")
        link    = item.get("link", "")
        lines.append(f"- {title}: {snippet} ({link})")

    return "\n".join(lines)