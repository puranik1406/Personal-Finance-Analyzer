import sys
import os
# Add the parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import multiprocessing
import time
import requests

def run_server():
    from app.main import app
    uvicorn.run(app, host="127.0.0.1", port=5001, log_level="debug")

if __name__ == '__main__':
    # Start server in a separate process
    p = multiprocessing.Process(target=run_server)
    p.start()
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        print("Making request to http://127.0.0.1:5001/ ...")
        res = requests.get("http://127.0.0.1:5001/", timeout=5)
        print("Status code:", res.status_code)
        if res.status_code != 200:
            print("Response:", res.text)
    except Exception as e:
        print("Request failed:", e)
    finally:
        p.terminate()
