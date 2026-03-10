from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get weather of a city"""
    return f"The weather in {city} is sunny."
