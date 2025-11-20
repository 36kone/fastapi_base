import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends

from app.dependencies.authentication import get_auth_user
from app.models import User
from app.schemas import (
    ConfigTableResponse,
    CreateConfigTable,
    UpdateConfigTable,
    ConfigTableValueResponse,
    ConfigTableSearchRequest,
    PaginatedResponse,
    MessageSchema,
    ConfigTableGetValuesRequest,
)
from app.services.config_table.config_table_service import ConfigTableService
from app.db.database import get_db

config_table_router = APIRouter()
logger = logging.getLogger("config-table")


@config_table_router.post("/", status_code=201, response_model=ConfigTableResponse)
def create_config(
    config: CreateConfigTable, current_user: User = Depends(get_auth_user)
):
    try:
        with get_db() as db:
            service = ConfigTableService(db)

            return service.create(config)
    except HTTPException as exc:
        logging.info(f"[CREATE CONFIG TABLE] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[CREATE CONFIG TABLE] -> {e}")
        raise e


@config_table_router.get("/", response_model=list[ConfigTableResponse])
def read_configs(
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = ConfigTableService(db)

            return service.read()
    except HTTPException as exc:
        logging.info(f"[READ CONFIG TABLE] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[READ CONFIG TABLE] -> {e}")
        raise e


@config_table_router.get("/{id_}", response_model=ConfigTableResponse)
def get_config_by_id(
    id_: UUID,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = ConfigTableService(db)

            return service.get_by_id(id_)
    except HTTPException as exc:
        logging.info(f"[GET CONFIG TABLE BY ID] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[GET CONFIG TABLE BY ID] -> {e}")
        raise e


@config_table_router.post(
    "/search", status_code=200, response_model=PaginatedResponse[ConfigTableResponse]
)
async def search_parameters(
    request: ConfigTableSearchRequest,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = ConfigTableService(db)

            items, total = await service.search(
                keyword=request.keyword,
                size=request.size,
                page=request.page,
            )

        return PaginatedResponse.create(
            total=total,
            page=request.page,
            size=request.size,
            items=[ConfigTableResponse.model_validate(i, from_attributes=True) for i in items],
        )
    except HTTPException as exc:
        logging.info(f"[SEARCH_CUSTOMERS] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[SEARCH_CUSTOMERS] -> {e}")
        raise e


@config_table_router.get("/value/{key}", response_model=ConfigTableValueResponse)
def get_config_value_by_key(
    key: str,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = ConfigTableService(db)

            value = service.get_value(key)

            return {"value": value}
    except HTTPException as exc:
        logging.info(f"[GET CONFIG TABLE BY KEY] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[GET CONFIG TABLE BY KEY] -> {e}")
        raise e


@config_table_router.post("/values", response_model=dict[str, str])
def get_values_by_keyword(
    data: ConfigTableGetValuesRequest,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = ConfigTableService(db)

            return service.get_values_by_keyword(data.keyword)
    except HTTPException as exc:
        logging.info(f"[GET CONFIG TABLE BY KEYWORD] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[GET CONFIG TABLE BY KEYWORD] -> {e}")
        raise e


@config_table_router.put("/{id_}", response_model=ConfigTableResponse)
def update_config(
    data: UpdateConfigTable,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = ConfigTableService(db)

            return service.update(data)
    except HTTPException as exc:
        logging.info(f"[UPDATE CONFIG TABLE] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[UPDATE CONFIG TABLE] -> {e}")
        raise e


@config_table_router.delete("/{id_}", response_model=MessageSchema)
def delete_config(
    id_: UUID,
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = ConfigTableService(db)

            return service.delete(id_)
    except HTTPException as exc:
        logging.info(f"[UPDATE CONFIG TABLE] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[UPDATE CONFIG TABLE] -> {e}")
        raise e
