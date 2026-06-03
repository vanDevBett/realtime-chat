from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.core.database import Base, engine
from app.core.exceptions import add_exception_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Realtime Chat API",
    description="Realtime chat API with WebSockets and Redis pub/sub",
    version="1.0.0"
)

add_exception_handlers(app)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])


@app.get("/")
def root():
    return {"message": "Realtime Chat API is running"}