from fastapi import APIRouter

clients_router = APIRouter()


@clients_router.get("/")
async def clients():
    return {"clients test"}
