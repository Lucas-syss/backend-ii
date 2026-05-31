import asyncio
import time

async def fetch_data(name: str, delay: float) -> str:
    """Simulates a data-fetching task."""
    await asyncio.sleep(delay)
    return f"{name} fetched in {delay:.1f}s"

async def rate_limited_task(semaphore: asyncio.Semaphore, name: str, delay: float) -> str:
    """Acquires the semaphore before running, enforcing max concurrency."""
    async with semaphore:
        result = await fetch_data(name, delay)
        return result

async def main():
    max_concurrent = 3
    task_count = 9

    semaphore = asyncio.Semaphore(max_concurrent)

    tasks = [
        rate_limited_task(semaphore, f"Request-{i}", 0.5)
        for i in range(1, task_count + 1)
    ]

    start = time.perf_counter()
    results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start

    for result in results:
        print(result)

    print(f"\n{task_count} tasks, max {max_concurrent} concurrent: {elapsed:.2f}s total")
    print(f"Expected minimum: {(task_count / max_concurrent) * 0.5:.1f}s (3 batches of {max_concurrent})")

asyncio.run(main())
