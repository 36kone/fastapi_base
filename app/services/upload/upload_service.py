import uuid
from app.core.config import settings

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.dependencies.exception_utils import ensure_400
from app.services.bucket.base import BucketService


class UploadService:
    def __init__(self, session: Session):
        self.session = session

    async def upload(self, type_: str, file: UploadFile, bucket: BucketService):
        folder_name = str(uuid.uuid4())

        if file.content_type not in ["video/mp4", "image/png", "image/jpeg"]:
            ensure_400(True, "Invalid file format. Only MP4, PNG or JPEG are allowed.")

        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > (500 * 1024 * 1024):
            ensure_400(True, "File too large, maximum of 500MB.")

        match type_:
            case "":
                pass
            case _:
                ensure_400(True, "Invalid type parameter.")

        extension = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{extension}"
        file_path = f"{type_}/{folder_name}/{filename}"

        try:
            bucket.upload(
                file_obj=file.file,
                filename=file_path,
                content_type=file.content_type,
                public=True,
            )
        except Exception as e:
            ensure_400(True, f"Failed to upload: {str(e)}")

        updated_data = None

        match type_:
            case "":
                pass
            case _:
                ensure_400(True, "Unsupported type for update.")

        if not updated_data:
            ensure_400(True, "Error updating data, update date is empty.")

        return {
            "message": "Upload successful!",
            "path": f"{settings.BUCKET_ENDPOINT}/{settings.BUCKET_NAME}/{file_path}",
        }
