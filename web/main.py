from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from databroker import DataBroker
from datacapture import DataCapture

# Cregs change model
class CregsChange(BaseModel):
    changed: list
    commit_to_flash: bool

# App and serial setup
app = FastAPI()
cregs = None


# DataBroker instance
dbroker = DataBroker()
# Create 'captures' directory
DataCapture.create_capture_directory()

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
        cregs = {"status": "ok", "cregs": dbroker.com.get_cregs_dict()}
    return JSONResponse(content=cregs)

@app.post("/api/cregschange", response_class=JSONResponse)
async def post(cregs_change: CregsChange):
    global cregs
    for c in cregs_change.changed:
        register = c["register"].lower()
        field = c["field"].upper()
        value = c["value"]
        try:
            dbroker.com.set_register_var_value(register, field, value)
            if cregs_change.commit_to_flash:
                dbroker.com.commit_settings()
            cregs = {"status": "ok", "cregs": dbroker.com.get_cregs_dict()}
            return cregs
        except:
           return {"status": "error"}
        
@app.get("/api/startcapture", response_class=JSONResponse)
async def get():
    status = await dbroker.start_capture()    
    if status:
        return {"status": "ok"}
    else:
        return {"status": "already running"}

@app.get("/api/stopcapture", response_class=JSONResponse)
async def get():
    status = await dbroker.stop_capture()
    if status:
        return {"status": "ok"}
    else:
        return {"status": "was not running"}

@app.get("/settings", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})

# Static files
app.mount("/", StaticFiles(directory="static", html = True), name="static")
