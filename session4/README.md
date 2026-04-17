# Session 4: Multi-processing in Python 🚀

## What is Multi-processing?

Think of the CPU as having multiple workers (cores). Normally, Python only lets **one worker do one thing at a time** (because of something called the GIL). Multi-processing breaks this limitation by spinning up **completely separate Python programs** (processes), each with their own worker and their own memory.

> **Simple analogy:** Threading is like one chef multitasking in a kitchen. Multi-processing is like hiring several chefs, each with their own kitchen.

---

## Threading vs Multi-processing

| | Threading | Multi-processing |
|---|---|---|
| Memory | Shared | Separate (each process has its own) |
| GIL affected? | Yes ❌ | No ✅ |
| Best for | I/O tasks (files, network, waiting) | CPU-heavy tasks (math, data crunching) |
| Overhead | Low | Higher (spawning a process costs more) |
| Communication | Easy (shared variables) | Harder (need special tools like Queue/Pipe) |

---

## The GIL — Why it matters

The **Global Interpreter Lock (GIL)** is a lock inside Python that allows only **one thread to run Python code at a time**, even on a multi-core machine.

- For **I/O-bound tasks** (waiting for a file, a network response), threading still works fine because the GIL is released while waiting.
- For **CPU-bound tasks** (heavy calculations), threading gives you **no real speedup** on multiple cores — the GIL blocks it.
- Multi-processing **bypasses the GIL entirely** because each process is a separate Python interpreter.

---

## When should you use Multi-processing?

✅ Use it when:
- You're doing **heavy number crunching** (scientific computing, simulations)
- You're processing **large datasets** in parallel
- You need **true parallelism** across CPU cores
- Your tasks are **independent** (don't need to share much data)

❌ Avoid it when:
- Your task is mostly **waiting** (use `asyncio` or threading instead)
- You need **lots of shared state** between workers (communication overhead becomes a bottleneck)
- Your tasks are **very short** (the overhead of spawning processes isn't worth it)

---

## How it works — Step by Step

### 1. Basic Process Creation

```python
import multiprocessing
import time

def compute_square(n):
    time.sleep(1)  # Simulate heavy computation
    print(f"Square of {n} is {n*n}")

if __name__ == "__main__":
    numbers = [2, 3, 4, 5]
    processes = []

    # Create and start a process for each number
    for number in numbers:
        p = multiprocessing.Process(target=compute_square, args=(number,))
        processes.append(p)
        p.start()  # Launch the process

    # Wait for all processes to finish
    for p in processes:
        p.join()
```

**Key things:**
- `target=` is the function each process will run
- `args=` passes arguments to that function (must be a tuple — note the comma in `(number,)`)
- `.start()` launches the process
- `.join()` makes the main program wait until that process finishes

---

## Pool — Managing Multiple Processes

When there's many tasks, manually creating and joining processes gets tedious. The `Pool` class manages a group of worker processes for you.

```python
import multiprocessing

def my_function(x):
    return x ** 2

if __name__ == "__main__":
    with multiprocessing.Pool() as pool:
        results = pool.map(my_function, [1, 2, 3, 4, 5])
    
    print(results)  # [1, 4, 9, 16, 25]
```

### Key Pool methods

| Method | What it does |
|---|---|
| `pool.map(func, iterable)` | Applies `func` to each item, returns results in order |
| `pool.map_async(func, iterable)` | Same but non-blocking |
| `pool.starmap(func, iterable)` | Like `map` but unpacks tuples as multiple arguments |
| `with multiprocessing.Pool() as pool:` | Auto-closes the pool when done (best practice) |

> By default, `Pool()` creates as many workers as your machine has CPU cores — which is usually optimal.

---

## Quick Reference Cheat Sheet

```python
# Single process
p = multiprocessing.Process(target=my_func, args=(arg1,))
p.start()
p.join()

# Multiple processes
processes = [multiprocessing.Process(target=f, args=(x,)) for x in items]
for p in processes: p.start()
for p in processes: p.join()

# Pool (recommended for many tasks)
with multiprocessing.Pool() as pool:
    results = pool.map(my_func, list_of_inputs)
```

---

## Common Pitfalls

1. **Forgetting `if __name__ == "__main__":`** — On Windows this causes infinite process spawning. Always include it.
2. **Trying to share regular variables** — Each process has its own memory. Changes in one process don't affect another. Use `multiprocessing.Queue` or `multiprocessing.Value` if you need shared state.
3. **Using multiprocessing for tiny tasks** — Spawning a process has overhead (~50-100ms). Not worth it for fast operations.
4. **Not calling `.join()`** — Without it, your main program can exit before child processes finish.