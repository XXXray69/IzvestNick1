from typing import Dict, Set
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.chat_connections: Dict[int, Set[WebSocket]] = {}

    async def connect(self, chat_id: int, websocket: WebSocket):
        await websocket.accept()
        self.chat_connections.setdefault(chat_id, set()).add(websocket)

    def disconnect(self, chat_id: int, websocket: WebSocket):
        if chat_id in self.chat_connections:
            self.chat_connections[chat_id].discard(websocket)
            if not self.chat_connections[chat_id]:
                self.chat_connections.pop(chat_id, None)

    async def broadcast(self, chat_id: int, payload: dict):
        dead = []
        for ws in self.chat_connections.get(chat_id, set()):
            try:
                await ws.send_json(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(chat_id, ws)


manager = ConnectionManager()
