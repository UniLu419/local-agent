"""Deprecated: tool definitions have moved to ``app/tools/``.

This module is kept for backward-compatibility only.  Import tools from the
new location instead:

    from app.tools.registry import get_tools          # all tools
    from app.tools.weather import get_weather         # individual tool
"""

# Re-export the moved symbol so any code that still imports from here works.
from app.tools.weather import get_weather  # noqa: F401

__all__ = ["get_weather"]
