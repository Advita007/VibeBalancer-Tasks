from fastapi import FastAPI
from datetime import datetime
import time
from typing import Optional
server_1 = FastAPI()
server_2 = FastAPI()
#SERVER 1
@server_1.get("/")
def home():
    return {"message": "Hello from server_1"}
@server_1.get("/info")
def get_info():
    return {"server":"1", "Current date and time:":str(datetime.now())}
@server_1.get("/work")
def work(delay: Optional[int] = None):
    if delay is None:
        delay = 0
    time.sleep(delay)
    return {"server":"1", "delay":str(delay),"status":"active"}
#SERVER 2
@server_2.get("/")
def home():
    return {"message": "Hello from server_2"}
@server_2.get("/info")
def get_info():
    return {"server":"2", "Current date and time:":str(datetime.now())}
@server_2.get("/work")
def work(delay: Optional[int] = None):
    if delay is None:
        delay = 0
    time.sleep(delay)
    return {"server":"2", "delay":str(delay),"status":"active"}