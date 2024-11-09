import hashlib
import random
import base64
import jwt
from datetime import datetime, timedelta, timezone
import json
from pydantic import BaseModel
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


HS256_SECRET_KEY = base64.b64encode(random.randbytes(64)).decode('utf-8')
ALGORITHM = 'HS256'
JWT_TOKEN_EXPIRE_MINUTES = timedelta(minutes=30)


with open('config.json', 'r') as file:
    user_db = json.load(file)['user_db']


class Token(BaseModel):
    access_token: str
    token_type: str


def get_password_hash(password: str, salt: bytes = None, iterations: int = None) -> str:
    if salt is None:
        salt = random.randbytes(16)
    if iterations is None:
        iterations = random.randint(10000, 100000)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
    return f'{iterations}${base64.b64encode(salt).decode('utf-8')}${base64.b64encode(hashed).decode('utf-8')}'


def verify_password(plain_password: str, hashed_password: str) -> bool:
    iterations, salt, hashed = hashed_password.split('$')
    hashed_from_plain_password = hashlib.pbkdf2_hmac('sha256', plain_password.encode(), base64.b64decode(salt), int(iterations))
    return base64.b64encode(hashed_from_plain_password).decode('utf-8') == hashed


def generate_token(payload: dict, hs256_secret_key: str = HS256_SECRET_KEY, expires_delta: timedelta | None = None) -> str:
    payload = payload.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload.update({'exp': int(expire.timestamp())})
    jwt_token = jwt.encode(payload, hs256_secret_key, algorithm=ALGORITHM)
    return jwt_token


def verify_token(jwt_token: str, hs256_secret_key: str = HS256_SECRET_KEY) -> bool:
    try:
        jwt.decode(jwt_token, hs256_secret_key, algorithms=[ALGORITHM])
        return True
    except:
        return False
    

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if verify_token(token, HS256_SECRET_KEY):
        pass
    else:
        raise credentials_exception


router = APIRouter()


@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    jwt_token = generate_token(user_db, HS256_SECRET_KEY)
    return Token(access_token=jwt_token, token_type='bearer')