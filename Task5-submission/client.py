import time
from fastapi import FastAPI
import concurrent.futures
import requests
from typing import Optional
from datetime import datetime

urls = []
for i in range(5):
    urls.append(f"http://127.0.0.1:8000/work?delay={i}&type=round_robin")
def send_request(url):
    response = requests.get(url)

start = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(send_request,urls)
finish = time.perf_counter()
print(f'Finished in {round(finish-start,2)} second(s): Load Balancer running on Round Robin Algorithm')

for i in range(5):
    urls.append(f"http://127.0.0.1:8000/work?delay={i}&type=least_connections")
def send_request(url):
    response = requests.get(url)

start = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(send_request,urls)
finish = time.perf_counter()
print(f'Finished in {round(finish-start,2)} second(s): Load Balancer running on Least Connections Algorithm')

## Observations:
''' Round Robin Algorithm (Static)
 The requests are equally distributed amomgst all the servers one after the other using the round robin algorithm. 
 The current load on the servers is not taken into account, resulting in poor load balancing/loss of efficiency at times.
 Least Connections Algorithm (Dynamic)
 The requests are not distributed equally as they are assigned based on the current number of requests assigned to a server (the ones it is already handling as well
 as those waiting in a queue). It adapts to varying delays as the pattern of number of active connections to a given server would vary. Moreover, faster servers are
 used more often as they will mostly have least the least number of active connections due to the speed of processing requests.
'''

