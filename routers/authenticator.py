import hashlib
import random
import base64
import jwt
from datetime import datetime, timedelta, timezone


HS256_SECRET_KEY = base64.b64encode(random.randbytes(64)).decode('utf-8')
ALGORITHM = 'HS256'
JWT_TOKEN_EXPIRE_MINUTES = timedelta(minutes=30)


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