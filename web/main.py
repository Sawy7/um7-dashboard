from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import asyncio
from um7 import UM7Communication
from typing import List
from threading import Lock

# Cregs change model
class CregsChange(BaseModel):
    changed: list
    commit_to_flash: bool

# App and serial setup
app = FastAPI()
com = UM7Communication("/dev/ttyUSB0")
cregs = None

class DataBroker:
    def __init__(self):
        self.ws_clients: List[WebSocket] = []
        self.client_lock = Lock()
        self.capture = None

    async def register(self, ws_client: WebSocket):
        await ws_client.accept()
        self.client_lock.acquire()
        initial_clients = len(self.ws_clients)
        self.client_lock.release()
        self.ws_clients.append(ws_client)
        print("initial clients", initial_clients)
        if initial_clients == 0:
            asyncio.ensure_future(self.run())

    def unregister(self, ws_client: WebSocket):
        self.ws_clients.remove(ws_client)

    async def run(self):
        while True:
            data = com.get_json_data()
            to_unregister = []
            for i,c in enumerate(self.ws_clients):
                try:
                    await c.send_text(str(data))
                except:
                    print("unregister", i)
                    to_unregister.append(c)
                    continue
                await asyncio.sleep(0.0)
            for c in to_unregister:
                self.unregister(c)
            if len(self.ws_clients) == 0:
                return

dbroker = DataBroker()

# Websocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await dbroker.register(websocket)
    try:
        await websocket.receive()
    except:
        # NOTE: Client was disconnected
        pass

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/cregs", response_class=JSONResponse)
async def get():
    global cregs
    if cregs is None:
        cregs = {"status": "ok", "cregs": com.get_cregs_dict()}
    return JSONResponse(content=cregs)

@app.post("/api/cregschange", response_class=JSONResponse)
async def post(cregs_change: CregsChange):
    global cregs
    for c in cregs_change.changed:
        register = c["register"].lower()
        field = c["field"].upper()
        value = c["value"]
        try:
            com.set_register_var_value(register, field, value)
            if cregs_change.commit_to_flash:
                com.commit_settings()
            cregs = {"status": "ok", "cregs": com.get_cregs_dict()}
            return cregs
        except:
           return {"status": "error"}
        
@app.get("/api/startcapture", response_class=JSONResponse)
async def get():
    pass

@app.get("/api/endcapture", response_class=JSONResponse)
async def get():
    pass

@app.get("/settings", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})

# Static files
app.mount("/", StaticFiles(directory="static", html = True), name="static")
