from fastapi import APIRouter

products_router = APIRouter()


@products_router.get("/")
async def products():
    return {"products test"}
