from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import os

from app.config import settings
from app.services import db_service
from app.services.ollama_service import ollama_service
from app.routes import upload, categorize, analyze, summary

app = FastAPI(
    title="Private Finance Analyzer",
    description="100% Local, Privacy-First Personal Finance AI powered by local Gemma",
    version="1.0.0"
)

# Enable CORS for local cross-origin development communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local ease-of-use
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create/Initialize SQLite Database on startup
@app.on_event("startup")
def on_startup():
    db_service.init_db()

# Mount Static Files (CSS, JS, images)
# Make sure static directory exists
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates rendering
templates = Jinja2Templates(directory="templates")

# Include backend API routers
app.include_router(upload.router)
app.include_router(categorize.router)
app.include_router(analyze.router)
app.include_router(summary.router)

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    """
    Serves the beautiful index.html page parsed via Jinja2 template engine.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/status")
async def get_ollama_status():
    """
    Endpoint to retrieve the connection status and list of installed models of the local Ollama API.
    """
    status = ollama_service.check_ollama_status()
    return status

if __name__ == '__main__':
    uvicorn.run(app, host=settings.host, port=settings.port)
