from datetime import datetime, UTC, timedelta
from typing import Any
from uuid import UUID

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.config import settings
from fastapi import Depends, HTTPException
from jose import jwt, JWTError

from db.database import get_db
from models.users.users import User
from schemas import Token
from schemas.users.user_schema import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
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
        }
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


def get_auth_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
    except Exception:
        raise credentials_exception

    query = select(User).where(User.id == user_id)

    user = db.scalar(query)

    if not user_id:
        raise credentials_exception
    return user
