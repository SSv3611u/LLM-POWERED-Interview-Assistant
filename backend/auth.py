import base64
import hashlib
import hmac
import json
import os
import time

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

import models
from database import get_db

security = HTTPBearer(auto_error=False)
_secret = os.getenv("AUTH_SECRET", "local-development-secret-change-me").encode()


def hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310000)
    return f"{salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    salt_hex, digest_hex = stored.split("$", 1)
    candidate = hash_password(password, bytes.fromhex(salt_hex)).split("$", 1)[1]
    return hmac.compare_digest(candidate, digest_hex)


def create_token(user_id: int) -> str:
    payload = json.dumps({"sub": user_id, "exp": int(time.time()) + 60 * 60 * 24 * 14}, separators=(",", ":")).encode()
    encoded = base64.urlsafe_b64encode(payload).decode().rstrip("=")
    signature = hmac.new(_secret, encoded.encode(), hashlib.sha256).hexdigest()
    return f"{encoded}.{signature}"


def _read_token(token: str) -> int:
    try:
        encoded, signature = token.rsplit(".", 1)
        expected = hmac.new(_secret, encoded.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise ValueError()
        payload = json.loads(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)))
        if payload["exp"] < time.time():
            raise ValueError()
        return int(payload["sub"])
    except (ValueError, KeyError, json.JSONDecodeError):
        raise HTTPException(status_code=401, detail="Your session has expired. Please sign in again.")


def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> models.User:
    if not credentials:
        raise HTTPException(status_code=401, detail="Sign in is required.")
    user = db.get(models.User, _read_token(credentials.credentials))
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return user
