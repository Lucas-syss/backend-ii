from fastapi import FastAPI
import asyncio

app = FastAPI()

async def fetch_user_data():
    """Simulates fetching user data from a database."""
    await asyncio.sleep(1)  
    return {"id": 1, "name": "Alice", "email": "alice@example.com"}

async def fetch_order_data():
    """Simulates fetching order data from an external service."""
    await asyncio.sleep(1.5)  
    return {"order_id": 42, "item": "Laptop", "status": "Shipped"}

@app.get("/dashboard")
async def get_dashboard():
    user, order = await asyncio.gather(
        fetch_user_data(),
        fetch_order_data()
    )
    return {
        "user": user,
        "order": order
    }
