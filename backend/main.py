from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

clients = {}
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str,WebSocket] = {}

    async def connect(self,client_id, websocket: WebSocket):
        if client_id in self.active_connections.keys():
            return False
        
        await websocket.accept()
        self.active_connections[client_id]=websocket

    async def send_personal_message(self, message: str,recv_id, websocket: WebSocket):
        if recv_id not in self.active_connections.keys():
            return "no user existing with reciever id entered"
        
        await self.active_connections[recv_id].send_text(message)

    async def disconnect_websocket(self,client_id, websocket: WebSocket):
        if client_id in self.active_connections.keys():
            if self.active_connections[client_id] is websocket:
                del self.active_connections[client_id]
        await websocket.close()
    async def send_msg(self,recv_id,msg):
        if recv_id in manager.active_connections.keys():
                await manager.active_connections[recv_id].send_text(f"recieved{msg}")


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def home():
    return Path(__file__).with_name("index.html").read_text(encoding="utf-8")


@app.websocket("/communicate/{client_id}/{recv_id}")
async def connect(websocket: WebSocket,client_id:str,recv_id:str):
    connected = await manager.connect(client_id,websocket)
    if not connected:
        await websocket.close(code=1008)
        return 
    manager.active_connections[client_id] = websocket

    # clients[client_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_msg(recv_id,data)

    except WebSocketDisconnect:
        manager.disconnect_websocket(client_id,websocket)
        # del manager.active_connections[client_id]
        return 
    finally:
        manager.disconnect_websocket(client_id,websocket)
