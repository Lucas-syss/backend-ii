import html
import re
from fastapi import FastAPI, Query
from pydantic import BaseModel, field_validator

app = FastAPI(
    title="Input Validation Demo",
    description="FastAPI endpoint that sanitises and validates user input",
)


class UserInput(BaseModel):
    username: str
    comment: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]{3,20}$", v):
            raise ValueError("Username must be 3–20 alphanumeric characters or underscores")
        return v

    @field_validator("comment")
    @classmethod
    def sanitise_comment(cls, v: str) -> str:
        sanitised = html.escape(v.strip())
        if len(sanitised) > 500:
            raise ValueError("Comment must be 500 characters or fewer")
        return sanitised


@app.post("/submit")
async def submit_input(data: UserInput):
    return {
        "username": data.username,
        "comment": data.comment,
        "message": "Input validated and sanitised successfully",
    }


@app.get("/search")
async def search(
    q: str = Query(..., min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9 ]+$")
):
    return {"query": q, "results": []}

# Run: uvicorn exercise:app --reload
# Test POST: curl -X POST http://localhost:8000/submit \
#   -H "Content-Type: application/json" \
#   -d '{"username": "alice", "comment": "<script>alert(1)</script>"}'
