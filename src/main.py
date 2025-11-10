from fastapi import FastAPI, Query
from typing import Optional
from src.service.time import get_current_time, get_greeting_message

app = FastAPI(title="Hello World API", version="1.0.0")


@app.get("/healthz")
async def healthz():
    """Health check endpoint for Kubernetes"""
    return {"status": "healthy"}


@app.get("/now")
async def get_now():
    """Returns current Costa Rica time in ISO format"""
    return {"now": get_current_time()}


@app.get("/hello")
async def hello(name: Optional[str] = Query(None, description="Name to greet")):
    """Returns a greeting based on current time of day in Costa Rica timezone"""
    message = get_greeting_message(name)
    return {"message": message}

