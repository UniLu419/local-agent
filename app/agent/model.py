import os

# Avoid inheriting shell SOCKS/HTTP proxies for localhost Ollama calls.
for key in (
    "ALL_PROXY",
    "all_proxy",
    "HTTP_PROXY",
    "http_proxy",
    "HTTPS_PROXY",
    "https_proxy",
):
    os.environ.pop(key, None)

from langchain_ollama import ChatOllama  # noqa: E402
from app.core.config import settings  # noqa: E402


def get_llm() -> ChatOllama:
    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=settings.ollama_temperature,
    )

