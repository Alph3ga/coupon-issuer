# src/middleware/jwt_auth.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Annotated, cast

from fastapi import Depends, HTTPException, Request, status
from fastapi.security.utils import get_authorization_scheme_param
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from starlette.types import ASGIApp

from src.auth.utils import validate_jwt

log = logging.Logger(__name__)


@dataclass(frozen=True)
class UserClaims:
    flatNumber: str
    isAdmin: bool
    userId: str


class JWTAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        authorization: str | None = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)

        # If no auth header or not Bearer, just continue without claims.
        if not authorization or scheme.lower() != "bearer" or not token:
            log.warning(
                "Authorization token not present for user, requesting"
                f"{request.method} {request.url}"
            )
            return await call_next(request)

        try:
            payload = validate_jwt(token)  # raises ValueError on invalid/expired
            flat_number = payload.get("flat_number")
            is_admin = payload.get("is_admin")
            user_id = payload.get("user_id")

            if (
                not isinstance(flat_number, str)
                or not isinstance(is_admin, bool)
                or not isinstance(user_id, str)
            ):
                log.error(
                    f"Invalid claims attached to request: {request.method} {request.url}\n \
                    Token: {token}"
                )
                raise ValueError("Missing or invalid claims in token")

            # Attach typed claims to request.state
            request.state.user_claims = UserClaims(
                flatNumber=flat_number, isAdmin=is_admin, userId=user_id
            )

        except ValueError as exc:
            # Invalid or expired token
            raise HTTPException(status_code=401, detail=str(exc)) from exc

        return await call_next(request)


def get_current_user(request: Request) -> UserClaims:
    """Dependency that returns typed user claims"""
    claims = cast(UserClaims | None, getattr(request.state, "user_claims", None))
    if claims is None:
        log.warning("User claims not valid/not found, redirected to log in page")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not logged in",
        )
    return claims


def require_admin(user: Annotated[UserClaims, Depends(get_current_user)]) -> UserClaims:
    """Dependency that ensures the current user is an admin."""
    if not user.isAdmin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
