from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.db.database import get_db
from app.dependencies.authentication import auth_guard
from app.schemas import (
    UserResponse,
    CreateUser,
    UpdateUser,
    MessageSchema,
    PaginatedResponse,
)
from app.schemas.users.user_schema import UserSearchRequest
from app.services.user.user_service import UserService

user_router = APIRouter(dependencies=[Depends(auth_guard)])


@user_router.post("/", status_code=201, response_model=UserResponse)
def create_user(
    data: CreateUser,
):
    try:
        with get_db() as db:
            service = UserService(db)

            return service.create(data)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@user_router.get("/", status_code=200, response_model=list[UserResponse])
def read_users():
    try:
        with get_db() as db:
            service = UserService(db)

            return service.read()
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@user_router.get("/{id_}", status_code=200, response_model=UserResponse)
def get_user_by_id(
    id_: UUID,
):
    try:
        with get_db() as db:
            service = UserService(db)

            return service.get_by_id(id_)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@user_router.get("/user/{email}", status_code=200, response_model=UserResponse)
def get_user_by_email(
    email: str,
):
    try:
        with get_db() as db:
            service = UserService(db)

            return service.get_by_email(email)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@user_router.post(
    "/search", status_code=200, response_model=PaginatedResponse[UserResponse]
)
async def search_users(
    search_request: UserSearchRequest,
):
    try:
        with get_db() as db:
            service = UserService(db)

            items, total = await service.search(
                keyword=search_request.keyword,
                page=search_request.page,
                size=search_request.size,
            )

            return PaginatedResponse.create(
                total=total,
                page=search_request.page,
                size=search_request.size,
                items=[
                    UserResponse.model_validate(i, from_attributes=True) for i in items
                ],
            )
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@user_router.put("/{id_}", status_code=200, response_model=UserResponse)
def update_user(
    data: UpdateUser,
):
    try:
        with get_db() as db:
            service = UserService(db)

            return service.update(data)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e


@user_router.delete("/{id_}", status_code=200, response_model=MessageSchema)
def delete_user(
    id_: UUID,
):
    try:
        with get_db() as db:
            service = UserService(db)

            return service.delete(id_)
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise e
