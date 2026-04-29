import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import Optional

users_db = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        if id not in users_db:
            return None
        data = users_db[id]
        return User(id=id, name=data["name"], email=data["email"])

@strawberry.type
class Mutation:
    @strawberry.mutation
    def update_name(self, id: int, new_name: str) -> Optional[User]:
        if id not in users_db:
            return None
        users_db[id]["name"] = new_name
        data = users_db[id]
        return User(id=id, name=data["name"], email=data["email"])

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_router = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_router, prefix="/graphql")

