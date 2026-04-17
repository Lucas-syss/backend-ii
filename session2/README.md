# Session 2: Design Patterns in Python 🏗️

## What are Design Patterns?

Design patterns are **proven, reusable solutions to common software problems**. They're not code you copy-paste — they're blueprints for how to structure your code in situations that come up again and again.

> **Simple analogy:** A design pattern is like a recipe. You don't invent from scratch how to make pasta — you follow a known structure and adapt it to your ingredients.

They were formalised in the famous "Gang of Four" book and are grouped into three categories:

| Category | Purpose | Examples |
|---|---|---|
| **Creational** | How objects are created | Singleton, Factory |
| **Structural** | How objects are composed | Adapter, Decorator |
| **Behavioural** | How objects communicate | Observer, Strategy |

---

## Pattern 1: Singleton

### The Problem
Sometimes you need **exactly one instance** of a class shared across your whole program — a database connection, a config manager, a logger. If you accidentally create two, you get inconsistent state.

### The Solution
Override `__new__` to return the same instance every time.

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

# Test
a = Singleton()
b = Singleton()
print(a is b)  # True — same object!
```

### When to use it
- **Database connection pool** — one shared connection
- **Configuration manager** — one place to read settings
- **Logger** — one consistent logging object

### Watch out for
- Singletons can make testing harder (shared state between tests)
- They're essentially global variables — use sparingly

---

## Pattern 2: Factory

### The Problem
You need to create objects of different types based on some condition, but you don't want the rest of your code to care about *which* type it gets — just that it gets *something* that works.

### The Solution
A factory function (or class) centralises object creation and returns the right type.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14159 * self.radius ** 2

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2

def shape_factory(shape_type, size):
    shapes = {"circle": Circle, "square": Square}
    if shape_type not in shapes:
        raise ValueError(f"Unknown shape: {shape_type}")
    return shapes[shape_type](size)

# Usage — caller doesn't need to know the class names
s1 = shape_factory("circle", 5)
s2 = shape_factory("square", 4)
print(s1.area())  # 78.53975
print(s2.area())  # 16
```

### When to use it
- Creating objects whose **exact type is determined at runtime** (e.g., based on user input or config)
- When you want to **hide implementation details** from the caller
- **Plugin systems** where new types can be registered and created by name

---

## Pattern 3: Observer

### The Problem
One object changes state, and several other objects need to know about it — but you don't want the subject to be tightly coupled to its observers.

### The Solution
The subject keeps a list of observers. When something changes, it calls `notify()` on all of them.

```python
class Subject:
    def __init__(self):
        self._observers = []
        self._state = None

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self._state)

    def set_state(self, state):
        self._state = state
        self.notify()  # Automatically tell everyone

class Observer:
    def __init__(self, name):
        self.name = name
    def update(self, state):
        print(f"{self.name} received update: {state}")

# Usage
subject = Subject()
subject.attach(Observer("Observer A"))
subject.attach(Observer("Observer B"))
subject.set_state("active")
```

### When to use it
- **Event systems** — UI buttons, keyboard/mouse input
- **Real-time dashboards** — multiple views updating when data changes
- **Pub/sub messaging** — multiple subscribers to one data source

---

## When to Use Which Pattern

| Situation | Pattern |
|---|---|
| Need exactly one instance of something | Singleton |
| Creating objects whose type varies at runtime | Factory |
| Multiple things need to react to one thing changing | Observer |
| Wrapping an incompatible interface | Adapter |
| Adding behaviour to an object dynamically | Decorator |

---

## Common Pitfalls

1. **Overusing Singleton** — Not everything needs to be global. Prefer dependency injection when possible.
2. **Factory overkill** — If you only ever create one type of object, a factory adds complexity for no gain.
3. **Observer memory leaks** — If observers aren't removed when no longer needed, they stay in memory. Always implement a `detach()` method.
4. **Patterns for patterns' sake** — Don't force a pattern if simple code solves the problem. Patterns exist to solve pain, not to show off.