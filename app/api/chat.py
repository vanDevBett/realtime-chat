import asyncio
import json

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db, SessionLocal
from app.core.security import decode_access_token
from app.services import user_service, chat_service, redis_service

router = APIRouter()


async def get_user_from_token(token: str, db: Session):
    payload = decode_access_token(token)
    if not payload:
        return None
    email = payload.get("sub")
    if not email:
        return None
    return user_service.get_user_by_email(db, email)


@router.get("/rooms/{room}/messages")
def get_room_messages(
    room: str,
    db: Session = Depends(get_db)
):
    return chat_service.get_room_messages(db, room)


@router.websocket("/ws/{room}")
async def websocket_endpoint(
    websocket: WebSocket,
    room: str,
    token: str = Query(...)
):
    db = SessionLocal()
    try:
        user = await get_user_from_token(token, db)
        if not user:
            await websocket.close(code=4001)
            return

        await websocket.accept()

        pubsub = await redis_service.subscribe_to_room(room)

        async def receive_messages():
            try:
                while True:
                    data = await websocket.receive_text()
                    message_data = json.loads(data)
                    saved = chat_service.save_message(
                        db,
                        content=message_data["content"],
                        room=room,
                        user_id=user.id
                    )
                    await redis_service.publish_message(room, {
                        "id": saved.id,
                        "content": saved.content,
                        "room": room,
                        "user_id": user.id,
                        "full_name": user.full_name,
                        "created_at": saved.created_at.isoformat()
                    })
            except WebSocketDisconnect:
                pass

        async def broadcast_messages():
            try:
                async for message in pubsub.listen():
                    if message["type"] == "message":
                        await websocket.send_text(message["data"])
            except Exception:
                pass

        await asyncio.gather(
            receive_messages(),
            broadcast_messages()
        )

    finally:
        await pubsub.unsubscribe(room)
        db.close()