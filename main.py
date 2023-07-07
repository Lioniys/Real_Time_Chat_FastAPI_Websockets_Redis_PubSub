from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import redis.asyncio as redis
from datetime import datetime
import asyncio
import json
from src.schemas import PydanticMessage, Event
from src.settings import REDIS_URL
from src.tasks import save_message_to_db

app = FastAPI()
r = redis.from_url(REDIS_URL)


async def websocket_loop(websocket: WebSocket, pubsub):
    while True:
        data = await websocket.receive_json()
        if data.get("event") == Event.FIRST.value:
            channels = data.get("channels")
            if channels:
                await pubsub.subscribe(*channels)
        if data.get("event") == Event.NEXT.value:
            datetime_now = datetime.now().isoformat(timespec='minutes')
            pydantic_message = PydanticMessage(datetime=datetime_now, **data.get("message"))
            await r.publish(pydantic_message.channel, json.dumps(pydantic_message.dict()))
            save_message_to_db.delay(pydantic_message.dict())


async def redis_pubsub_loop(websocket: WebSocket, pubsub):
    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            message = message["data"].decode()
            await websocket.send_json(message)


@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        async with r.pubsub() as pubsub:
            await pubsub.subscribe('')
            await asyncio.gather(
                websocket_loop(websocket=websocket, pubsub=pubsub),
                redis_pubsub_loop(websocket=websocket, pubsub=pubsub)
            )
    except WebSocketDisconnect:
        pass
