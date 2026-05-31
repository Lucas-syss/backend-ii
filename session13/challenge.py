import logging
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Best Practices API",
    description="FastAPI with CORS, request logging, error handling, and Pydantic models",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    logger.info("--> %s %s", request.method, request.url.path)
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    logger.info("<-- %s in %.3fs", response.status_code, elapsed)
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    return response


class Item(BaseModel):
    name: str
    value: float


items_db: dict[int, Item] = {}
_counter = 0


@app.get("/")
async def index():
    return {"message": "Hello from FastAPI with best practices"}


@app.post("/items", status_code=201)
async def create_item(item: Item):
    global _counter
    _counter += 1
    items_db[_counter] = item
    logger.info("Created item %d: %s", _counter, item.name)
    return {"id": _counter, "item": item}


@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return items_db[item_id]


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s: %s", request.url.path, exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# Run: uvicorn challenge:app --reload
# Docs: http://localhost:8000/docs
