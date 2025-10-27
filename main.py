from fastapi import FastAPI

from controllers.router import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api")
