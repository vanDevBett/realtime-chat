from sqlalchemy.orm import Session

from app.models.message import Message


def save_message(db: Session, content: str, room: str, user_id: int) -> Message:
    message = Message(
        content=content,
        room=room,
        user_id=user_id
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_room_messages(db: Session, room: str, limit: int = 50) -> list:
    messages = (
        db.query(Message)
        .filter(Message.room == room)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": msg.id,
            "content": msg.content,
            "room": msg.room,
            "user_id": msg.user_id,
            "full_name": msg.user.full_name,
            "created_at": msg.created_at.isoformat()
        }
        for msg in reversed(messages)
    ]