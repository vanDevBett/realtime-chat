import json
import redis.asyncio as aioredis

from app.core.config import settings

redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)


async def publish_message(room: str, message: dict) -> None:
    await redis_client.publish(room, json.dumps(message))


async def subscribe_to_room(room: str):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(room)
    return pubsub