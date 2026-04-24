# Session 7: Logging in Python 📋

## What is Logging?

Logging records what your application is doing at runtime — errors, warnings, and general events. It's the difference between knowing *why* your app crashed in production vs guessing.

> **Don't use `print()`** for this. Print statements vanish when your app runs as a service. Logs persist to files, can be filtered by severity, and include timestamps automatically.

---

## Log Levels

From least to most severe:

| Level | When to use |
|---|---|
| `DEBUG` | Detailed dev info — variable values, step traces |
| `INFO` | Normal events — app started, user logged in |
| `WARNING` | Something unexpected but non-breaking |
| `ERROR` | Something failed — caught exception |
| `CRITICAL` | App is about to crash |

Setting a level means you see that level **and everything above it**. Set `INFO` and you won't see `DEBUG` noise in production.

---

## Built-in `logging` Module

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'   # omit this to print to console
)

logging.debug("Checking value...")
logging.info("App started")
logging.warning("Disk space low")
logging.error("Failed to connect to DB")
logging.critical("System shutting down")
```

**Output in `app.log`:**
```
2024-01-15 10:23:01,234 - DEBUG - Checking value...
2024-01-15 10:23:01,235 - INFO - App started
2024-01-15 10:23:01,235 - WARNING - Disk space low
2024-01-15 10:23:01,236 - ERROR - Failed to connect to DB
2024-01-15 10:23:01,236 - CRITICAL - System shutting down
```

### Logging Exceptions

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    logging.exception("Division failed")  # automatically includes the traceback
```

---

## `loguru` — Simpler Alternative

```bash
pip install loguru
```

```python
from loguru import logger

# Log to file with automatic rotation
logger.add("app.log", rotation="1 MB", retention="7 days", level="DEBUG")

logger.debug("Checking value...")
logger.info("App started")
logger.warning("Disk space low")
logger.error("Failed to connect to DB")
```

`loguru` requires zero configuration out of the box — it logs to the console by default with colours and formatting already set up. `logger.add()` adds a file destination on top.

---

## Built-in vs loguru

| | `logging` | `loguru` |
|---|---|---|
| Setup required | Yes | Minimal |
| File rotation | Manual (handlers) | Built-in |
| Coloured output | No | Yes |
| Exception tracing | Basic | Rich |
| Standard library | Yes | Third-party |

Use `logging` when working on libraries or projects that can't have extra dependencies. Use `loguru` for applications where developer experience matters.

---

## Quick Reference

```python
# Built-in — log to file
logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# loguru — log to file with rotation
from loguru import logger
logger.add("app.log", rotation="1 MB")

# Both support the same level calls:
logger.debug / logger.info / logger.warning / logger.error / logger.critical
```