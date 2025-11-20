import logging

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from app.db.database import get_db
from app.dependencies.authentication import get_auth_user
from app.models import User
from app.schemas import UploadMessage
from app.services.upload.upload_service import UploadService
from app.services.bucket.base import BucketService
from app.services.bucket.factory import get_bucket_service

upload_router = APIRouter()
logger = logging.getLogger("upload")


@upload_router.post("/{type_}", status_code=200, response_model=UploadMessage)
async def upload(
    type_: str,
    file: UploadFile = File(...),
    bucket: BucketService = Depends(get_bucket_service),
    current_user: User = Depends(get_auth_user),
):
    try:
        with get_db() as db:
            service = UploadService(db)

            return await service.upload(type_, file, bucket)
    except HTTPException as exc:
        logging.info(f"[UPLOAD] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[UPLOAD] -> {e}")
        raise e
