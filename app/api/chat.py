import json
from collections.abc import Iterator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.agent.model import get_llm
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.openai import ChatCompletionRequest


router = APIRouter()
llm = get_llm()


def _content_to_text(content: object) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    return json.dumps(content, ensure_ascii=False, default=str)


def stream_agent(message: str):
    for chunk in llm.stream(message):
        text = _content_to_text(chunk.content)
        if text:
            yield f"data: {text}\n\n"
    yield "data: [DONE]\n\n"


@router.post("/v1/chat/completions")
def chat(req: ChatRequest):
    if req.stream:
        return StreamingResponse(
            stream_agent(req.message),
            media_type="text/event-stream",
        )