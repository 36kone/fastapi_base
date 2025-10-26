from typing import TypeVar, Optional
from fastapi import HTTPException, status, FastAPI, Request
from starlette.responses import JSONResponse

T = TypeVar("T")


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        if isinstance(exc, HTTPException):
            raise exc
        return JSONResponse(
            status_code=400,
            content={"detail": "Ops... Algo deu errado."},
        )


# ✅ Garante que um objeto existe ou levanta 400
def ensure_or_400(
    obj: Optional[T], message: str = "Recurso inválido ou inexistente"
) -> T:
    if not obj:
        raise HTTPException(status_code=400, detail=message)
    return obj


def ensure_400(obj: Optional[T], message: str = "Recurso inválido ou inexistente") -> T:
    if obj:
        raise HTTPException(status_code=400, detail=message)
    return obj


# ✅ Garante que um objeto existe ou levanta 401
def ensure_or_401(
    obj: Optional[T], message: str = "Recurso inválido ou inexistente"
) -> T:
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return obj


# ✅ Garante que um objeto existe ou levanta 404
def ensure_or_404(obj: Optional[T], message: str = "Recurso não encontrado") -> T:
    if not obj:
        raise HTTPException(status_code=404, detail=message)
    return obj


def ensure_or_400_json(obj: Optional[T], message: dict = "Recurso não encontrado") -> T:
    if not obj:
        raise HTTPException(status_code=404, detail=message)
    return obj


def ensure_2_obj_or_400_json(
    obj1: Optional[T], obj2: Optional[T], message: dict = "Recurso não encontrado"
) -> T:
    if not obj1 and not obj2:
        raise HTTPException(status_code=404, detail=message)
    return obj1, obj2


# ✅ Garante que uma lista exista ou levanta 404
def ensure_list_or_404(obj: list, message: str = "Not found"):
    if not obj:
        raise HTTPException(status_code=404, detail=message)
    return obj


# ✅ Garante que um objeto existe ou levanta 403
def ensure_or_403(obj: Optional[T], message: str = "Acesso negado") -> T:
    if not obj:
        raise HTTPException(status_code=403, detail=message)
    return obj


# ✅ Valida uma condição booleana, senão levanta 400
def assert_or_400(condition: bool, message: str = "Dados inválidos"):
    if not condition:
        raise HTTPException(status_code=400, detail=message)


# ✅ Valida uma condição booleana, senão levanta 403
def assert_or_403(condition: bool, message: str = "Ação não permitida"):
    if not condition:
        raise HTTPException(status_code=403, detail=message)


# ✅ Valida uma condição booleana, senão levanta 422
def assert_or_422(condition: bool, message: str = "Dados inválidos ou incompletos"):
    if not condition:
        raise HTTPException(status_code=422, detail=message)


# ✅ Garante que um valor esteja presente, senão levanta 422
def require(value: Optional[T], message: str = "Campo obrigatório") -> T:
    if not value:
        raise HTTPException(status_code=422, detail=message)
    return value
