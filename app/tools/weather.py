from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city.

    NOTE: This is a mock implementation. Replace the body with a call to a
    real weather API (e.g. OpenWeatherMap) when an API key is available.

    Args:
        city: The name of the city to look up.

    Returns:
        A weather summary string for the requested city.
    """
    # TODO: Replace with real API call, e.g.:
    #   import requests
    #   resp = requests.get(
    #       "https://api.openweathermap.org/data/2.5/weather",
    #       params={"q": city, "appid": os.getenv("OPENWEATHER_API_KEY"), "units": "metric"},
    #   )
    #   data = resp.json()
    #   return f"{data['weather'][0]['description']}, {data['main']['temp']}°C"
    return f"The weather in {city} is sunny and 22°C."
