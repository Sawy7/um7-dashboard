from fastapi import WebSocket
from typing import List
import asyncio
from threading import Lock

from um7 import UM7Communication
from datacapture import DataCapture

class DataBroker:
    def __init__(self):
        self.com = UM7Communication("/dev/ttyUSB0")
        self.ws_clients: List[WebSocket] = []
        self.client_lock = Lock()
        self.capture = None

    def count_clients(self):
        client_count = len(self.ws_clients)
        if self.capture is not None:
            client_count += 1
        return client_count

    async def register(self, ws_client: WebSocket):
        await ws_client.accept()
        self.client_lock.acquire()
        initial_clients = self.count_clients()
        self.ws_clients.append(ws_client)
        self.client_lock.release()
        if initial_clients == 0:
            asyncio.ensure_future(self.run())

    def unregister(self, ws_client: WebSocket):
        self.ws_clients.remove(ws_client)

    async def start_capture(self):
        self.client_lock.acquire()
        if self.capture is not None:
            self.client_lock.release()
            return False
        initial_clients = self.count_clients()
        self.capture = DataCapture()
        self.client_lock.release()
        if initial_clients == 0:
            asyncio.ensure_future(self.run())
        return True

    async def stop_capture(self):
        self.client_lock.acquire()
        self.capture = None
        self.client_lock.release()

    async def run(self):
        while True:
            data = self.com.get_json_data()
            to_unregister = []
            for i,c in enumerate(self.ws_clients):
                try:
                    await c.send_text(str(data))
                except:
                    print("unregister", i)
                    to_unregister.append(c)
                    continue
            if self.capture is not None:
                await self.capture.write(str(data))
            for c in to_unregister:
                self.unregister(c)
            if len(self.ws_clients) == 0 and self.capture is None:
                return
            await asyncio.sleep(0.0)