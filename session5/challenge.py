from fastapi import FastAPI
import aiohttp
import asyncio
import time

app = FastAPI()

URLS = [
    "https://example.com",
    "https://httpbin.org/get",
    "https://jsonplaceholder.typicode.com/posts/1",
]

async def fetch_page(session, url):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            html = await response.text()
            return {
                "url": url,
                "status": response.status,
                "content_length": len(html),
                "ok": True
            }
    except Exception as e:
        return {
            "url": url,
            "status": None,
            "content_length": 0,
            "ok": False,
            "error": str(e)
        }

@app.get("/scrape")
async def scrape():
    start = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url) for url in URLS]
        results = await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start

    return {
        "results": results,
        "total_urls": len(results),
        "successful": sum(1 for r in results if r["ok"]),
        "elapsed_seconds": round(elapsed, 2)
    }

