from app.schemas.base import BaseSchema


class MessageSchema(BaseSchema):
    message: str


class UploadMessage(BaseSchema):
    message: str
    path: str
