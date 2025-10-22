from fastapi import APIRouter

orders_router = APIRouter()


@orders_router.get("/")
async def orders():
    return {"orders test"}
