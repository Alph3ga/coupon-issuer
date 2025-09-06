# src/auth/jwt_utils.py

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from src.settings import JWT_SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360  # 6 hour default


def create_jwt(
    flat_number: str, is_admin: bool, user_id: str, expires_delta: timedelta | None = None
) -> str:
    """Create a JWT with flatNumber and isAdmin claims."""
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode: dict[str, Any] = {
        "flat_number": flat_number,
        "is_admin": is_admin,
        "user_id": user_id,
        "exp": expire,
    }
    assert JWT_SECRET_KEY
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)


def validate_jwt(token: str) -> dict[str, str | bool]:
    """Validate a JWT and return the decoded payload if valid. Raises jwt exceptions if invalid."""
    try:
        assert JWT_SECRET_KEY
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        flat_number: str = payload.get("flat_number")
        is_admin: bool = payload.get("is_admin")
        user_id: str = payload.get("user_id")

        if flat_number is None or is_admin is None:
            raise jwt.InvalidTokenError("Missing claims in token")

        return {"flat_number": flat_number, "is_admin": is_admin, "user_id": user_id}

    except jwt.ExpiredSignatureError as e:
        raise ValueError("Token has expired") from e
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {e}") from e
