# Session 3: Multi-threading in Python 🧵

## What is Multi-threading?

A **thread** is a lightweight unit of execution that runs inside your program. Multi-threading means running multiple threads at the same time, so different parts of your code can make progress concurrently.

> **Simple analogy:** A single-threaded program is one person doing tasks one by one. Multi-threading is one person juggling tasks — while waiting for the kettle to boil, you prep the cups. You're not faster at each task, but you stop wasting waiting time.

---

## The GIL — Python's Big Caveat

Python has a **Global Interpreter Lock (GIL)** — a mechanism that ensures only **one thread executes Python code at a time**, even on a multi-core CPU.

This means:
- For **CPU-heavy tasks** (math, processing), threading gives **no speedup** — only one thread runs at a time anyway → use **multiprocessing** instead
- For **I/O-bound tasks** (waiting for files, network, databases), threading **works great** — while one thread waits, another can run → the GIL is released during I/O

---

## Threading vs Multiprocessing vs AsyncIO

| | Threading | Multiprocessing | AsyncIO |
|---|---|---|---|
| GIL affected? | Yes | No | Yes |
| Memory | Shared | Separate | Shared |
| Best for | I/O-bound tasks | CPU-bound tasks | Many concurrent I/O tasks |
| Overhead | Low | High | Very low |
| Complexity | Medium | Medium | Higher |

**Rule of thumb:**
- Downloading files, querying a DB, handling network requests → **Threading**
- Number crunching, image processing, heavy computation → **Multiprocessing**
- Thousands of simultaneous lightweight I/O operations → **AsyncIO**

---

## How Threading Works

### Basic thread creation

```python
import threading
import time

def print_numbers():
    for i in range(5):
        print(f"Number: {i}")
        time.sleep(1)

def print_letters():
    for letter in "ABCDE":
        print(f"Letter: {letter}")
        time.sleep(1)

# Create threads
t1 = threading.Thread(target=print_numbers)
t2 = threading.Thread(target=print_letters)

# Start both
t1.start()
t2.start()

# Wait for both to finish
t1.join()
t2.join()

print("Both threads complete.")
```

The two functions run **interleaved** — while `print_numbers` sleeps for 1 second, `print_letters` runs, and vice versa.

---

## Key Threading Concepts

### `.start()` vs `.join()`
- `.start()` — launches the thread and returns immediately (doesn't wait)
- `.join()` — blocks the main program until that thread finishes

### `args` and `kwargs`
```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

t = threading.Thread(target=greet, args=("Alice",), kwargs={"greeting": "Hi"})
t.start()
t.join()
```

### Daemon threads
A daemon thread is automatically killed when the main program exits — useful for background tasks that shouldn't block shutdown.
```python
t = threading.Thread(target=background_task, daemon=True)
t.start()
# Main program exits → daemon thread is killed automatically
```

---

## Thread Safety — Shared Memory Problem

Because threads share memory, **two threads modifying the same variable simultaneously** can cause bugs called **race conditions**.

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(100000):
        counter += 1  # Not thread-safe! Read-modify-write is three steps

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)
t1.start(); t2.start()
t1.join(); t2.join()

print(counter)  # Probably NOT 200000!
```

### Fix: Use a Lock
```python
lock = threading.Lock()

def increment_safe():
    global counter
    for _ in range(100000):
        with lock:          # Only one thread can be here at a time
            counter += 1
```

---

## When to Use Threading

✅ Use it when:
- Tasks spend most of their time **waiting** (network requests, file reads, DB queries)
- You want to **keep a UI responsive** while doing background work
- You need **simple concurrency** without the overhead of separate processes

❌ Avoid it when:
- Tasks are **CPU-intensive** (the GIL prevents real parallelism)
- **Shared state is complex** (race conditions become hard to debug)
- You need **thousands of concurrent tasks** (use `asyncio` instead)

---

## Quick Reference Cheat Sheet

```python
import threading

# Create and run a thread
t = threading.Thread(target=my_func, args=(arg1,))
t.start()
t.join()  # Wait for it to finish

# Multiple threads
threads = [threading.Thread(target=f, args=(x,)) for x in items]
for t in threads: t.start()
for t in threads: t.join()

# Thread-safe shared variable
lock = threading.Lock()
with lock:
    shared_variable += 1  # Only one thread at a time
```

## Common Pitfalls

1. **Forgetting `.join()`** — The main program might exit before threads finish.
2. **Race conditions** — Multiple threads reading and writing the same variable without a lock causes unpredictable results.
3. **Using threading for CPU tasks** — Won't speed anything up due to the GIL; use `multiprocessing` instead.
4. **Deadlocks** — Two threads each waiting for a lock held by the other. Avoid by always acquiring locks in the same order.