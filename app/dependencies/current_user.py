from typing import Annotaded

from fastapi import Depends

from app.dependencies.authentication import get_auth_user
from app.models import User

CurrentUser = Annotaded[User, Depends(get_auth_user)]
