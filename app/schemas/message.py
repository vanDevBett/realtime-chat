from datetime import datetime
from pydantic import BaseModel


class MessageResponse(BaseModel):
    id: int
    content: str
    room: str
    user_id: int
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    content: str
    room: str