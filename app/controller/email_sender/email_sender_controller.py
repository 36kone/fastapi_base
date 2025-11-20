import logging

from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.schemas import SendEmailRequest, MessageSchema

from app.dependencies.email import EmailSender

email_sender_router = APIRouter()


@email_sender_router.post(
    "/send-email", status_code=200, response_model=MessageSchema
)
async def send_email(data: SendEmailRequest, background_tasks: BackgroundTasks):
    try:
        email_sender = EmailSender()

        background_tasks.add_task(
            email_sender.send_email,
            data.subject,
            data.email_to,
            data.template_path,
            data.context
        )
        return {"message": "Email sent successfully."}
    except HTTPException as exc:
        logging.info(f"[WEB - SEND_EMAIL] -> {exc}")
        raise exc
    except Exception as e:
        logging.info(f"[WEB - SEND_EMAIL] -> {e}")
        raise e
