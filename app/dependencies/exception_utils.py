from typing import TypeVar
from fastapi import HTTPException, status, FastAPI
from starlette.responses import JSONResponse

T = TypeVar("T")


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def generic_exception_handler(exc: Exception):
        if isinstance(exc, HTTPException):
            raise exc
        return JSONResponse(
            status_code=400,
            content={"detail": "Ops... Algo deu errado."},
        )


def ensure_or_400(
    obj: T, message: str = "Recurso inválido ou inexistente"
) -> T:
    if not obj:
        raise HTTPException(status_code=400, detail=message)
    return obj


def ensure_400(obj: T, message: str = "Recurso inválido ou inexistente") -> T:
    if obj:
        raise HTTPException(status_code=400, detail=message)
    return obj


def ensure_or_401(
    obj: T, message: str = "Recurso inválido ou inexistente"
) -> T:
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return obj


def ensure_or_404(obj: T, message: str = "Recurso não encontrado") -> T:
    if not obj:
        raise HTTPException(status_code=404, detail=message)
    return obj


def ensure_or_400_json(obj: T, message: str = "Recurso não encontrado") -> T:
    if not obj:
        raise HTTPException(status_code=404, detail=message)
    return obj


def ensure_list_or_404(obj: list, message: str = "Not found"):
    if not obj:
        raise HTTPException(status_code=404, detail=message)
    return obj


def ensure_or_403(obj: T, message: str = "Acesso negado") -> T:
    if not obj:
        raise HTTPException(status_code=403, detail=message)
    return obj


def assert_or_400(condition: bool, message: str = "Dados inválidos"):
    if not condition:
        raise HTTPException(status_code=400, detail=message)


def assert_or_403(condition: bool, message: str = "Ação não permitida"):
    if not condition:
        raise HTTPException(status_code=403, detail=message)


def assert_or_422(condition: bool, message: str = "Dados inválidos ou incompletos"):
    if not condition:
        raise HTTPException(status_code=422, detail=message)


def require(value: T, message: str = "Campo obrigatório") -> T:
    if not value:
        raise HTTPException(status_code=422, detail=message)
    return value
