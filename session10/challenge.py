from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

SECRET_KEY = "change-this-to-a-long-random-secret-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="JWT Auth Demo",
    description="FastAPI with hashed passwords, JWT tokens, and protected routes",
)

# In-memory user store (use a real DB in production)
fake_users_db: dict[str, dict] = {
    "alice": {
        "username": "alice",
        "hashed_password": pwd_context.hash("secret123"),
    },
    "bob": {
        "username": "bob",
        "hashed_password": pwd_context.hash("bobpass"),
    },
}


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc
    if username not in fake_users_db:
        raise credentials_exc
    return User(username=username)


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/secure-data")
async def secure_data(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}! This is protected data."}


@app.get("/public")
async def public():
    return {"message": "This endpoint is public and requires no authentication."}

# Run: uvicorn challenge:app --reload
# Get token: curl -X POST http://localhost:8000/token \
#   -d "username=alice&password=secret123"
# Use token: curl http://localhost:8000/secure-data \
#   -H "Authorization: Bearer <token>"
