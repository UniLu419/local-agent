from datetime import datetime, timezone

from langchain_core.tools import tool


@tool
def get_current_datetime(tz: str = "local") -> str:
    """Get the current date and time.

    Args:
        tz: Timezone to use. Pass "utc" for UTC, or "local" for the system's local time.

    Returns:
        A human-readable string with the current date, time, weekday, and timezone.
    """
    if tz.lower() == "utc":
        now = datetime.now(tz=timezone.utc)
        tz_label = "UTC"
    else:
        now = datetime.now()
        tz_label = "local time"

    return (
        f"{now.strftime('%A, %Y-%m-%d %H:%M:%S')} ({tz_label})"
    )
