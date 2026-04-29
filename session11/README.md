# Session 11: Building GraphQL APIs with Python 🍓

## What is GraphQL?

GraphQL is a **query language for APIs**. Instead of the server deciding what data to return, the **client asks for exactly what it needs** — no more, no less.

> **REST vs GraphQL in one example:**
> - REST: `GET /users/1` → returns id, name, email, address, phone, avatar... (everything)
> - GraphQL: ask for `{ user(id: 1) { name } }` → returns only `name`

This eliminates over-fetching (too much data) and under-fetching (needing multiple requests to get all the data you want).

---

## Core Concepts

| Concept | What it does | REST equivalent |
|---|---|---|
| **Query** | Read data | GET |
| **Mutation** | Write / update data | POST / PUT / DELETE |
| **Type** | Shape of your data | Response schema |
| **Resolver** | Function that returns the data | Controller / handler |
| **Schema** | The full API contract | API spec |

Everything in GraphQL goes through **one endpoint** — typically `/graphql`.

---

## Setup

```bash
pip install strawberry-graphql fastapi uvicorn
```

---

## Defining Types and Resolvers with Strawberry

```python
import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL

@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User:
        # In a real app, you'd fetch from a database here
        return User(id=id, name="Alice", email="alice@example.com")

schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)

# Run: uvicorn filename:app --reload
# GraphQL playground: http://127.0.0.1:8000/graphql
```

**Client query:**
```graphql
{
  user(id: 1) {
    name
    email
  }
}
```

**Response:**
```json
{
  "data": {
    "user": {
      "name": "Alice",
      "email": "alice@example.com"
    }
  }
}
```

---

## Mutations — Writing Data

Mutations change data. They're defined in a separate `Mutation` class:

```python
@strawberry.type
class Mutation:
    @strawberry.mutation
    def update_name(self, id: int, new_name: str) -> User:
        # Update in DB, return updated object
        return User(id=id, name=new_name, email="alice@example.com")

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

**Client mutation:**
```graphql
mutation {
  updateName(id: 1, newName: "Bob") {
    id
    name
  }
}
```

---

## Strawberry vs Graphene

| | Strawberry | Graphene |
|---|---|---|
| Style | Decorator + type hints | Class-based |
| Python feel | Modern (dataclass-like) | More verbose |
| FastAPI integration | First-class | Manual setup |
| Async support | Built-in | Limited |

Strawberry is the current recommendation for new projects.

---

## Quick Reference

```python
# Type definition
@strawberry.type
class MyType:
    field_name: str

# Query resolver
@strawberry.type
class Query:
    @strawberry.field
    def my_query(self, arg: int) -> MyType:
        return MyType(field_name="value")

# Mutation resolver
@strawberry.type
class Mutation:
    @strawberry.mutation
    def my_mutation(self, arg: str) -> MyType:
        return MyType(field_name=arg)

# Schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
```