from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="Hello World API",
    description="A minimal FastAPI application following web development best practices",
    version="1.0.0",
)


class HealthResponse(BaseModel):
    status: str
    version: str


class MessageResponse(BaseModel):
    message: str


@app.get("/", response_model=MessageResponse)
async def index():
    return {"message": "Hello from FastAPI"}


@app.get("/health", response_model=HealthResponse)
async def health():
    return {"status": "ok", "version": "1.0.0"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# Run: uvicorn exercise:app --reload
# Docs: http://localhost:8000/docs
