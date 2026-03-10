from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.core.config import settings

app = FastAPI()
app.include_router(chat_router)


def main():
    import uvicorn

    uvicorn.run("app.main:app", host=settings.api_host, port=settings.api_port)


if __name__ == "__main__":
    main()

