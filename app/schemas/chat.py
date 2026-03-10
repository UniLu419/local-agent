from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    message: str
    stream: bool = False


class ChatResponse(BaseModel):
    reply: str
