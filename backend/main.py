from fastapi import FastAPI,WebSocket,Request,WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
# @app.websocket("/ws")
# async def websocket_endpoint(websocket:WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await websocket.send_text(f"Echo{data}")
#     except WebSocketDisconnect:
#         print("client disconnected  ")



class ConnectionManager:
    def __init__(self):
        self.active_connections = []


    async def connect(self,websocket:WebSocket):
        await websocket.accept()    
        self.active_connections.append(websocket)
    async def send_personal_message(self,message:str,websocket:WebSocket):
        await websocket.send_text(message)

    def disconnect_websocket(self,websocket:WebSocket):
        self.active_connections.remove(websocket)    


manager = ConnectionManager()


@app.websocket("/communicate")
async def connect(websocket:WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Recieved: {data}",websocket)
    except WebSocketDisconnect:
        manager.disconnect_websocket(websocket)
        await manager.send_personal_message("bye",websocket)
