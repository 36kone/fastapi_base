import logging

from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.schemas import SendEmailRequest, MessageSchema

from app.dependencies.email import EmailSender

email_sender_router = APIRouter()


@email_sender_router.post(
    "/send-email",
    status_code=200,
    response_model=MessageSchema,
    summary="Send email",
    description="""
    Send an email using a specified HTML template and context parameters.

    - **subject**: The subject line of the email.
    - **email_to**: The recipient's email address.
    - **template_path**: The file path to the HTML template that will be rendered as the email body.
    - **context**: A dictionary of variables to populate the placeholders in the HTML template.
    """
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
