# from uuid import UUID

# from fastapi import Request
# from pydantic.v1 import EmailStr
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

# from models import User

# from core.config import settings
from app.dependencies.exception_utils import ensure_or_400

# from schemas import (
#    UserResponse,
#    Token,
#    ChangePasswordRequest,
#    PasswordResetRequest,
#    PasswordResetConfirm
# )
from app.core.security import (
    verify_password,
    # get_password_hash,
)
from app.dependencies.authentication import create_user_access_token
from app.services.user.user_service import UserService


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(self.db)

    def login(self, form_data: OAuth2PasswordRequestForm):
        user = self.user_service.get_by_email(form_data.username)

        ensure_or_400(
            verify_password(form_data.password, user.password),
            "Invalid password",
        )

        return create_user_access_token(user)

    # def change_password(
    #         self,
    #         data: ChangePasswordRequest,
    #         user_id: UUID,
    #         db: DBSession,
    # ):
    #     current_user = self.user_service.get_by_id(user_id)
    #     ensure_or_400(
    #         verify_password(data.current_password, current_user.password),
    #         "Current password is incorrect",
    #    )
    #
    #     current_user.password = get_password_hash(data.new_password)
    #    db.commit()
    #    db.refresh(current_user)
    #
    #    return {"message": "Password changed successfully"}

    # async def request_password_reset(
    #         self,
    #         data: PasswordResetRequest,
    #         db: DBSession,
    # ):
    #     user = ensure_or_404(self.user_service.get_by_email(str(data.email)))
    #
    #     reset_token = secrets.token_urlsafe(32)
    #     await update_user_password_reset_token(
    #        email=data.email, token=reset_token, session=db
    #    )

    #    reset_url = f"{settings.CRM_URL or 'http://localhost:8080'}/reset-password?token={reset_token}"

    #    email_sender = EmailSender()
    #    await email_sender.send_email(
    #        subject="Recuperação de Senha",
    #        email_to=data.email,
    #        template_path="app/templates/password_reset.html",
    #        context={"username": user.name, "reset_url": reset_url},
    #    )
    #    return {"message": "Email for reset password sent successfully"}

    # async def confirm_password_reset(
    #         self,
    #         data: PasswordResetConfirm,
    #         db: DBSession,
    # ):
    #    user = ensure_or_400(
    #        await get_user_by_password_reset_token(data.token, db),
    #        "Token inválido ou expirado",
    #    )
    #    await update_user_password(user, data.new_password, db)
    #     return {"message": "Senha redefinida com sucesso"}
