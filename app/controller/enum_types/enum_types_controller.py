import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends

from app.dependencies.authentication import get_auth_user
from app.schemas import (
    EnumTypesSchema,
    EnumTypesResponse,
    MessageSchema,
    EnumTypesUpdate,
)
from app.models import User
from app.services.enum_types.enum_types_service import EnumTypesService
from app.db.database import get_db

enum_types_router = APIRouter()
logger = logging.getLogger("enum-types")


@enum_types_router.post("/", status_code=201, response_model=EnumTypesResponse)
def create_enum_types(
    enum_types: EnumTypesSchema, current_user: User = Depends(get_auth_user)
):
    try:
        with get_db() as db:
            service = EnumTypesService(db)

            return service.create(enum_types)
    except HTTPException as exc:
        logging.info(f"[CREATE_ENUM_TYPE] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[CREATE_ENUM_TYPE] -> {e}")
        raise e


@enum_types_router.get("/", status_code=200, response_model=list[EnumTypesResponse])
def read_enum_types(current_user: User = Depends(get_auth_user)):
    try:
        with get_db() as db:
            service = EnumTypesService(db)

            return service.read()
    except HTTPException as exc:
        logging.info(f"[READ_ENUM_TYPES] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[READ_ENUM_TYPES] -> {e}")
        raise e


@enum_types_router.get(
    "/type/{type}", status_code=200, response_model=list[EnumTypesResponse]
)
def get_enum_types_by_type(type: str, current_user: User = Depends(get_auth_user)):
    try:
        with get_db() as db:
            service = EnumTypesService(db)

            return service.get_by_type(type)
    except HTTPException as exc:
        logging.info(f"[GET_ENUM_TYPE_BY_TYPE] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[GET_ENUM_TYPE_BY_TYPE] -> {e}")
        raise e


@enum_types_router.get("/{id}", status_code=200, response_model=EnumTypesResponse)
def get_enum_type_by_id(id: UUID, current_user: User = Depends(get_auth_user)):
    try:
        with get_db() as db:
            service = EnumTypesService(db)

            return service.get_by_id(id)
    except HTTPException as exc:
        logging.info(f"[GET_ENUM_TYPE_BY_ID] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[GET_ENUM_TYPE_BY_ID] -> {e}")
        raise e


@enum_types_router.put("/{id}", status_code=200, response_model=EnumTypesResponse)
def update_enum_type(
    data: EnumTypesUpdate, current_user: User = Depends(get_auth_user)
):
    try:
        with get_db() as db:
            service = EnumTypesService(db)

            return service.update(data)
    except HTTPException as exc:
        logging.info(f"[UPDATE_ENUM_TYPE] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[UPDATE_ENUM_TYPE] -> {e}")
        raise e


@enum_types_router.delete("/{id}", status_code=200, response_model=MessageSchema)
def delete_enum_type(id: UUID, current_user: User = Depends(get_auth_user)):
    try:
        with get_db() as db:
            service = EnumTypesService(db)

            return service.delete(id)
    except HTTPException as exc:
        logging.info(f"[DELETE_ENUM_TYPE] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[DELETE_ENUM_TYPE] -> {e}")
        raise e
