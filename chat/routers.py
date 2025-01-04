from fastapi import WebSocket, WebSocketDisconnect, APIRouter


from users.models import User
from db import SessionLocal

router = APIRouter(
    prefix='',
    tags=['chat']
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = {}
        self.active_connections[user_id][user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].pop(user_id, None)
            if not self.active_connections[user_id]:
                self.active_connections.pop(user_id)

    async def send_personal_message(self, message: str, recipient_id: int):
        recipient_websocket = self.active_connections.get(recipient_id, {}).get(recipient_id)
        if recipient_websocket:
            await recipient_websocket.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/{user_id}/{recipient_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, recipient_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        await websocket.close()
        return

    username = user.name
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"{username}: {data}", recipient_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
