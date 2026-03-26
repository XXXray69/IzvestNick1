from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket_manager import manager

router = APIRouter(tags=['ws'])


@router.websocket('/ws/chats/{chat_id}')
async def chat_ws(websocket: WebSocket, chat_id: int):
    await manager.connect(chat_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({'event': 'echo', 'payload': data})
    except WebSocketDisconnect:
        manager.disconnect(chat_id, websocket)
