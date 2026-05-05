from fastapi import FastAPI
from fastapi import Response
import requests
import time
from datetime import datetime
from typing import Optional
lb = FastAPI()
visited = 0
servers = ["http://127.0.0.1:8001/work", "http://127.0.0.1:8003/work"]
connections = {"http://127.0.0.1:8001/work": 0,"http://127.0.0.1:8003/work": 0}

@lb.get("/work")

def work(delay:Optional[int] = None, type:Optional[str] = None):
    if(type=="round_robin"):
            global visited
            target_url = f"{servers[visited]}?delay={delay}"
            print(f"RR: Request sent to Server {visited +1}")
            visited = (visited + 1) % len(servers)
            server_response = requests.get(target_url)
            return Response(content=server_response.content,status_code=server_response.status_code)
    
    elif(type=="least_connections"):
          least_val = min(connections["http://127.0.0.1:8001/work"],connections["http://127.0.0.1:8003/work"])
          if(least_val == connections["http://127.0.0.1:8001/work"]):
                base_url = "http://127.0.0.1:8001/work"
                print("LC: Request sent to Server 1")
          
          else:
                base_url = "http://127.0.0.1:8003/work"
                print("LC: Request sent to Server 2")
          target_url = f"{base_url}?delay={delay}"
          connections[base_url]+=1
          print(f"Number of active connections on Server 1 = {connections['http://127.0.0.1:8001/work']} and Server 2 = {connections['http://127.0.0.1:8003/work']}")
          try:
               server_response = requests.get(target_url)
               return Response(content=server_response.content,status_code=server_response.status_code)
          finally:
                connections[base_url]-=1


      



