from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio
from um7 import UM7Communication

app = FastAPI()
com = UM7Communication("/dev/ttyUSB0")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = com.get_json_data()
            await websocket.send_text(str(data))
            await asyncio.sleep(0.0)
    except WebSocketDisconnect:
        pass

app.mount("/", StaticFiles(directory="static", html = True), name="static")

@app.get("/")
async def get():
    return FileResponse("index.html")

