import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from strawberry.types import Info
from typing import List, Optional

# --- In-memory data ---

users_db = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

posts_db = {
    1: [
        {"title": "GraphQL is great", "content": "Here's why..."},
        {"title": "Python tips",      "content": "Always use type hints."},
    ],
    2: [
        {"title": "Async Python",     "content": "Use asyncio for I/O."},
    ],
}

VALID_API_KEY = "secret-key-123"

# --- Types ---

@strawberry.type
class Post:
    title: str
    content: str

@strawberry.type
class User:
    id: int
    name: str
    email: str
    posts: List[Post]

# --- Auth helper ---

def get_api_key(info: Info) -> Optional[str]:
    request = info.context["request"]
    return request.headers.get("x-api-key")

# --- Query ---

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        if id not in users_db:
            return None
        data = users_db[id]
        user_posts = [Post(**p) for p in posts_db.get(id, [])]
        return User(id=id, name=data["name"], email=data["email"], posts=user_posts)

    @strawberry.field
    def all_users(self) -> List[User]:
        result = []
        for uid, data in users_db.items():
            user_posts = [Post(**p) for p in posts_db.get(uid, [])]
            result.append(User(id=uid, name=data["name"], email=data["email"], posts=user_posts))
        return result

# --- Mutation (authenticated) ---

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_post(self, info: Info, user_id: int, title: str, content: str) -> Optional[User]:
        api_key = get_api_key(info)
        if api_key != VALID_API_KEY:
            raise Exception("Unauthorised: invalid or missing API key")

        if user_id not in users_db:
            return None

        posts_db.setdefault(user_id, []).append({"title": title, "content": content})
        data = users_db[user_id]
        user_posts = [Post(**p) for p in posts_db[user_id]]
        return User(id=user_id, name=data["name"], email=data["email"], posts=user_posts)

# --- App ---

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)

# Run: uvicorn solution:app --reload
# Playground: http://127.0.0.1:8000/graphql