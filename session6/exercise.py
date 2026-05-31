import asyncio

async def task_function(name: str, delay: float) -> str:
    """Simulates an async task that takes a given amount of time."""
    await asyncio.sleep(delay)
    return f"{name} completed"

async def run_with_timeout(name: str, delay: float, timeout: float) -> str:
    """Runs a task and cancels it gracefully if it exceeds the timeout."""
    try:
        result = await asyncio.wait_for(
            asyncio.create_task(task_function(name, delay)),
            timeout=timeout,
        )
        return result
    except asyncio.TimeoutError:
        return f"{name} timed out after {timeout}s"

async def main():
    tasks_config = [
        ("Task A", 0.5, 1.0),
        ("Task B", 2.0, 1.0),  # will time out
        ("Task C", 0.8, 1.0),
        ("Task D", 3.0, 1.0),  # will time out
    ]

    tasks = [
        run_with_timeout(name, delay, timeout)
        for name, delay, timeout in tasks_config
    ]

    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

asyncio.run(main())
