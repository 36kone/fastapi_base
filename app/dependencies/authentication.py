from datetime import datetime, UTC, timedelta
from typing import Any, Callable
from uuid import UUID

from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from sqlalchemy import select

from app.core.config import settings
from fastapi import Depends, HTTPException, Security, Request
from jose import jwt, JWTError

from app.db.database import get_db
from app.models.users.users import User
from app.schemas.auth.auth_schema import Token
from app.schemas.users.user_schema import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
bearer_scheme = HTTPBearer(auto_error=False)


def create_access_token(data: dict, expires_delta: timedelta | None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_user_access_token(user):
    access_token = create_access_token(
        {
            "id": str(user.id),
            "username": str(user.email),
        },
        expires_delta=None,
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        dic_info = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id = dic_info.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Access denied, verify your token")
    if not user_id:
        raise HTTPException(
            status_code=401, detail="Access denied, verify the token expiration"
        )
    return


def get_auth_user(
    bearer: HTTPAuthorizationCredentials = Security(bearer_scheme),
    oauth2: str | None = Depends(oauth2_scheme),
) -> User:
    token = bearer.credentials if bearer else oauth2
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    try:
        user_id = UUID(payload.get("id"))
    except Exception as e:
        raise credentials_exception from e

    query = select(User).where(User.id == user_id)

    with get_db() as db:
        user = db.scalar(query)

    if not user_id:
        raise credentials_exception
    return user


def auth_guard(request: Request, user: User = Depends(get_auth_user)) -> None:
    endpoint = request.scope.get("endpoint")

    if not endpoint:
        return

    roles = getattr(endpoint, "__required_roles__", [])

    if roles and user.role not in roles:
        raise HTTPException(status_code=403, detail="Forbidden")


def required_permissions(*, roles: list[str] | None = None) -> Callable:
    def decorator(func: Callable):
        func.__required_roles__ = roles or []
        return func
    return decorator
