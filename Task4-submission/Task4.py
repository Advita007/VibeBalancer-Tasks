import time
from fastapi import FastAPI
import concurrent.futures
import requests
from typing import Optional
from datetime import datetime

server_1 = FastAPI()
#SERVER 1
@server_1.get("/")
def home():
    return {"message": "Hello from server_1"}
@server_1.get("/info")
def get_info():
    return {"server":"1", "Current date and time:":str(datetime.now())}
@server_1.get("/work")
def work(delay: Optional[int] = None):
    start_time = datetime.now()
    print(f"Request STARTED at: {start_time}",flush=True)
    if delay is None:
        delay = 0
    time.sleep(delay)
    end_time = datetime.now()
    duration = round((end_time - start_time).total_seconds(), 2)
    print(f"Request ended at: {end_time} with duration = {duration}",flush=True)
    return {"server":"1", "delay":str(delay),"status":"active"}

# In the week 3 server, the requests run one after the other, as the server is synchronous. The total time taken is atleast 6s, as the second request always has to wait until the first one is completed. The server is blocking.

url = "http://127.0.0.1:8001/work?delay=3"
start = time.perf_counter()
for _ in range(5):
    response = requests.get(url)
finish = time.perf_counter()
print(f'Finished in {round(finish-start,2)} second(s): Blocking behaviour')

urls = []
for i in range(5):
    urls.append("http://127.0.0.1:8002/work?delay=3")
    
def send_request(url):
    response = requests.get(url)

start = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(send_request,urls)
finish = time.perf_counter()
print(f'Finished in {round(finish-start,2)} second(s): Non-Blocking behaviour using multi-threading')