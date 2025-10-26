from datetime import datetime, timezone, timedelta

from core.config import settings
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from db.database import get_db
from main import oauth2_scheme


def create_access_token(user_id, expiration_time=timedelta(minutes=30)):
    data_expire = datetime.now(timezone.utc) + expiration_time
    dic_info = {"sub": str(user_id), "exp": data_expire}
    decoded = jwt.encode(dic_info, settings.SECRET_KEY, settings.ALGORITHM)
    return decoded


def verify_token(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)
):
    try:
        dic_info = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id = dic_info.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Access denied, verify your token")
    # user = session.query(User).filter(User.id == user_id).first()
    if not user_id:
        raise HTTPException(
            status_code=401, detail="Access denied, verify the token expiration"
        )
    return  # user
