from typing import Dict
from fastapi import WebSocket

class Manager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, token: str):
        await websocket.accept()
        self.active_connections[websocket] = token
    
    def disconnect(self, websocket: WebSocket):
        del self.active_connections[websocket]
    
    async def broadcast(self, msg: str):
        for user in self.active_connections.keys():
            await user.send_text(msg)

manager = Manager()  ## სინგლტონ
