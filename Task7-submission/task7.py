from fastapi import FastAPI
from fastapi import Response
import requests
import time
from datetime import datetime
from typing import Optional
from prometheus_client import Counter,Gauge,make_asgi_app
import psutil
import asyncio
import httpx
from contextlib import asynccontextmanager


visited = 0
servers = ["http://127.0.0.1:8001/work", "http://127.0.0.1:8003/work"]
connections = {"http://127.0.0.1:8001/work": 0,"http://127.0.0.1:8003/work": 0}
server_health = {
    "http://127.0.0.1:8001/work": True,
    "http://127.0.0.1:8003/work": True
}
request_counter = Counter("total_requests","Total number of requests sent to the load balancer")
total_errors_counter = Counter("total_errors","Total number of errors returned")
active_connections = Gauge("active_connections","Total number of active connections")
cpu_usage = Gauge("cpu_usage_percent","Current cpu usage percent")
memory_usage_percent = Gauge("memory_usage_percent","Current memory usage percent")

#health check
async def single_check(client, url):
    try:
        response = await client.get(url, timeout=3.0)
        response.raise_for_status()
        server_health[url] = True
    except Exception as e:
         server_health[url] = False

async def check_health():
    async with httpx.AsyncClient() as client:
        
        while True:
            cpu_usage.set(psutil.cpu_percent(interval=None))
            memory_usage_percent.set(psutil.virtual_memory().percent)

            tasks = [single_check(client, url) for url in servers]
            await asyncio.gather(*tasks)
            
            await asyncio.sleep(5)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the background task
    health_task = asyncio.create_task(check_health())
    yield
    # Clean up on shutdown
    health_task.cancel()

lb = FastAPI(lifespan=lifespan)

metrics_app = make_asgi_app()
lb.mount("/metrics",metrics_app)
client = httpx.AsyncClient()
                
@lb.get("/work")


async def work(delay:Optional[int] = None, type:Optional[str] = None):
      request_counter.inc()

      if(server_health["http://127.0.0.1:8001/work"]==True and server_health["http://127.0.0.1:8003/work"]==True):
          if(type=="round_robin"):
           
            global visited
            target_url = f"{servers[visited]}?delay={delay}"
            
            print(f"RR: Request sent to Server {visited +1}")
            active_connections.inc()
            try:
               server_response = await client.get(target_url, timeout=10.0)
               return Response(content=server_response.content, status_code=server_response.status_code)
            except:
               total_errors_counter.inc()
               target_url = f"{servers[(visited + 1) % len(servers)]}?delay={delay}"
               try:
                   server_response = await client.get(target_url, timeout=10.0)
                   return Response(content=server_response.content, status_code=server_response.status_code)
               except:
                   return "503 Service Unavailable"
            finally:
                visited = (visited + 1) % len(servers)
                active_connections.dec()
                
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
                active_connections.inc()
                print(f"Number of active connections on Server 1 = {connections['http://127.0.0.1:8001/work']} and Server 2 = {connections['http://127.0.0.1:8003/work']}")
                try:
                    server_response = await client.get(target_url, timeout=10.0)
                    return Response(content=server_response.content, status_code=server_response.status_code)
                except:
                    total_errors_counter.inc()
                    connections[base_url]-=1
                    if(base_url=="http://127.0.0.1:8003/work"):
                        base_url = "http://127.0.0.1:8001/work"
                    else:
                        base_url = "http://127.0.0.1:8003/work"
                        
                    target_url = f"{base_url}?delay={delay}"
                    connections[base_url]+=1
                    try:
                        server_response = await client.get(target_url, timeout=10.0)
                        return Response(content=server_response.content, status_code=server_response.status_code)
                    except:
                        return "503 Service Unavailable"
                finally:
                        connections[base_url]-=1
                        active_connections.dec()
          
      elif server_health["http://127.0.0.1:8001/work"] == False and server_health["http://127.0.0.1:8003/work"] == True:
            active_connections.inc()
            base_url = "http://127.0.0.1:8003/work"
            target_url = f"{base_url}?delay={delay}"
            try:
               server_response = await client.get(target_url, timeout=10.0)
               return Response(content=server_response.content, status_code=server_response.status_code)
            except:
               total_errors_counter.inc()
               base_url = "http://127.0.0.1:8001/work"
               target_url = f"{base_url}?delay={delay}"
               try:
                   server_response = await client.get(target_url, timeout=10.0)
                   return Response(content=server_response.content, status_code=server_response.status_code)
               except:
                   return "503 Service Unavailable"
            finally:
                active_connections.dec()

      elif server_health["http://127.0.0.1:8001/work"] == True and server_health["http://127.0.0.1:8003/work"] == False:
            active_connections.inc()
            base_url = "http://127.0.0.1:8001/work"
            target_url = f"{base_url}?delay={delay}"
            try:
               server_response = await client.get(target_url, timeout=10.0)
               return Response(content=server_response.content, status_code=server_response.status_code)
            except:
               total_errors_counter.inc()
               base_url = "http://127.0.0.1:8003/work"
               target_url = f"{base_url}?delay={delay}"
               try:
                   server_response = await client.get(target_url, timeout=10.0)
                   return Response(content=server_response.content, status_code=server_response.status_code)
               except:
                   return "503 Service Unavailable"

            finally:
                active_connections.dec()
      else:
          return "503 Service Unavailable"
          

      