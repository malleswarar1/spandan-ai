"""SPANDAN AI — Service Utilities"""
import os
from datetime import datetime, timedelta
from typing import Optional

SECRET_KEY = os.getenv("SECRET_KEY", "spandan-ai-secret-2024-change-in-prod")
ALGORITHM  = "HS256"
TOKEN_EXP_HOURS = 48

def hash_password(password: str) -> str:
    try:
        from passlib.context import CryptContext
        ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return ctx.hash(password)
    except Exception:
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain: str, hashed: str) -> bool:
    try:
        from passlib.context import CryptContext
        ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return ctx.verify(plain, hashed)
    except Exception:
        import hashlib
        return hashlib.sha256(plain.encode()).hexdigest() == hashed

def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    try:
        from jose import jwt
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(hours=TOKEN_EXP_HOURS))
        to_encode["exp"] = expire
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception:
        import base64, json, time
        payload = {**data, "exp": time.time() + TOKEN_EXP_HOURS * 3600}
        return base64.b64encode(json.dumps(payload).encode()).decode()

def decode_token(token: str) -> Optional[dict]:
    try:
        from jose import jwt, JWTError
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        try:
            import base64, json
            return json.loads(base64.b64decode(token.encode()).decode())
        except Exception:
            return None
