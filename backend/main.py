from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

clients = {}
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    def disconnect_websocket(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def home():
    return Path(__file__).with_name("index.html").read_text(encoding="utf-8")


@app.websocket("/communicate/{client_id}/{recv_id}")
async def connect(websocket: WebSocket,client_id:str,recv_id:str):
    await manager.connect(websocket)
    clients[client_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            if recv_id in clients.keys():
                await clients[recv_id].send_text(f"recieved{data}")

    except WebSocketDisconnect:
        manager.disconnect_websocket(websocket)
        del clients[client_id]
        return 
