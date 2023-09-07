from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
from um7 import UM7Communication

# App and serial setup
app = FastAPI()
com = UM7Communication("/dev/ttyUSB0")
cregs_settings = None

# Websocket endpoint
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

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html.jinja", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def get(request: Request):
    global cregs_settings
    if cregs_settings is None:
        cregs_settings = com.get_cregs()
    return templates.TemplateResponse("settings.html.jinja", {"request": request, "cregs": cregs_settings})

# Static files
app.mount("/", StaticFiles(directory="static", html = True), name="static")
