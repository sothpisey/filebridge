import hashlib
import random
import base64


def get_password_hash(password: str, salt: bytes = None, iterations: int = None) -> str:
    if salt is None:
        salt = random.randbytes(16)
    if iterations is None:
        iterations = random.randint(10000, 100000)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
    return f'pbkdf2_sha256${iterations}${base64.b64encode(salt).decode('utf-8')}${base64.b64encode(hashed).decode('utf-8')}'


def verify_password(plain_password: str, hashed_password: str) -> bool:
    algorithm, iterations, salt, hashed = hashed_password.split('$')
    hashed_from_plain_password = hashlib.pbkdf2_hmac('sha256', plain_password.encode(), base64.b64decode(salt), int(iterations))
    return base64.b64encode(hashed_from_plain_password).decode('utf-8') == hashed
