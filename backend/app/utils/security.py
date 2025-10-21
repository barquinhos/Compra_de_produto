import jwt
import os
import datetime as datetime
from passlib.context import CryptContext
from datetime import timedelta

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "chave_secreta_super_forte")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: dict, minutes: int | None = None) -> str:
    expire_delta = datetime.timedelta(minutes=minutes or ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_time = datetime.datetime.now(datetime.timezone.utc) + expire_delta
    
    to_encode = {"exp": expire_time, **subject}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None