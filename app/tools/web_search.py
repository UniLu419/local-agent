from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """Search the web for up-to-date information on a topic.

    Uses the DuckDuckGo Instant Answer API — no API key required.
    Returns a short abstract or a list of related topic snippets.

    Args:
        query: The search query string.

    Returns:
        A text summary of the top search results, or an error message.
    """
    try:
        import requests  # requests is a transitive dep of many packages; safe to import lazily

        resp = requests.get(
            "https://api.duckduckgo.com/",
            params={
                "q": query,
                "format": "json",
                "no_redirect": "1",
                "no_html": "1",
                "skip_disambig": "1",
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        # Prefer the direct abstract (Wikipedia-style answer)
        abstract = data.get("AbstractText", "").strip()
        if abstract:
            source = data.get("AbstractSource", "")
            return f"{abstract}\n\nSource: {source}" if source else abstract

        # Fall back to related topic snippets
        snippets: list[str] = []
        for topic in data.get("RelatedTopics", [])[:5]:
            if isinstance(topic, dict) and topic.get("Text"):
                snippets.append(topic["Text"])

        if snippets:
            return "\n\n".join(snippets)

        return "No results found for that query."

    except Exception as exc:
        return f"Web search failed: {exc}"
