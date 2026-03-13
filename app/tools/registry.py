"""Central tool registry.

Add new tools here so they are automatically picked up by the agent graph.
Each tool must be a LangChain @tool-decorated callable.
"""

from langchain_core.tools import BaseTool

from app.tools.calculator import calculator
from app.tools.datetime_tool import get_current_datetime
from app.tools.weather import get_weather
from app.tools.web_search import web_search


def get_tools() -> list[BaseTool]:
    """Return the list of all tools available to the agent."""
    return [
        calculator,
        get_current_datetime,
        get_weather,
        web_search,
    ]
