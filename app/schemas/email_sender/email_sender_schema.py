from pydantic import EmailStr

from app.schemas import BaseSchema


class SendEmailRequest(BaseSchema):
    subject: str
    email_to: EmailStr
    template_path: str
    context: dict