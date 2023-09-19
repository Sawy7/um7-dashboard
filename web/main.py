from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os, datetime

from databroker import DataBroker
from datacapture import DataCapture

# Cregs change model
class CregsChange(BaseModel):
    changed: list
    commit_to_flash: bool

# Time model
class Time(BaseModel):
    timestamp: float

def set_time(time: Time):
    timestamp = time.timestamp
    # Convert the timestamp to a datetime object
    dt = datetime.datetime.utcfromtimestamp(timestamp)
    # Format the datetime object as a string in the required format
    date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
    # Use the formatted date string to set the system time using the 'date' command
    try:
        os.system(f"sudo date -s '{date_str}'")
        return True
    except:
        return False

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
def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/captures")
def get(request: Request):
    return templates.TemplateResponse("captures.html", {"request": request, "file_list": DataCapture.list_captures(dbroker.capture)})

@app.get("/downloadcapture/{file_name}")
def download_file(file_name: str):
    return FileResponse(DataCapture.get_file_path(file_name))

@app.get("/api/cregs", response_class=JSONResponse)
def get():
    global cregs
    if cregs is None:
        cregs = {"status": "ok", "cregs": dbroker.com.get_cregs_dict()}
    return JSONResponse(content=cregs)

@app.post("/api/cregschange", response_class=JSONResponse)
def post(cregs_change: CregsChange):
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
        
@app.post("/api/startcapture", response_class=JSONResponse)
async def post(time: Time):
    status = set_time(time)
    if not status:
        return {"status": "timeerror"}
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

@app.get("/api/iscapturing", response_class=JSONResponse)
async def get():
    status = await dbroker.is_capturing()
    return {"status": status}

@app.get("/settings", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})

# Static files
app.mount("/", StaticFiles(directory="static", html = True), name="static")
