from typing import Any
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db_handler.user_login_handler import user_login_db_handler
from backend.models.database import get_db
from backend.schemas.user_login import SignUpSchema, SignUpResponseSchema, SignInResponseSchema, SignInSchema, \
    MsgSchema, ResetPasswordSchema
from backend.service.user_login import user_login_service
from backend.utils.email_utils import send_reset_password_email
from backend.utils.utils import generate_password_reset_token, verify_password_reset_token

auth_router = APIRouter(prefix="/api/v1/user", tags=["Authentication"])


@auth_router.post(
    "/sign-up",
    description="This API endpoint allows users to register and create an account by providing "
                "their registration details, including email and password.",
    status_code=status.HTTP_201_CREATED,
    response_model=SignUpResponseSchema,
    responses={
        409: {
            "description": "User with this email already exists",
            "content": {"application/json": {"example": {"detail": "User with this email already exists"}}},
        }
    }
)
def sign_up(
        request_payload: SignUpSchema,
        db: Session = Depends(get_db)
) -> Any:
    existing_user = user_login_db_handler.get_by_column(
        db=db, column_name='email', value=request_payload.email
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    return user_login_service.create_user(request_payload=request_payload, db=db)


@auth_router.post(
    "/sign-in",
    description="This API endpoint allows users to signin/login an account by providing "
                "their email and password.",
    status_code=status.HTTP_200_OK,
    response_model=SignInResponseSchema,
    responses={
        400: {
            "description": "Incorrect email/password",
            "content": {"application/json": {"example": {"detail": "Incorrect email/password"}}},
        }
    }
)
def sign_in(
        request_payload: SignInSchema,
        db: Session = Depends(get_db)
) -> Any:
    existing_user = user_login_db_handler.get_by_column(
        db=db, column_name='email', value=request_payload.email
    )
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email"
        )
    elif existing_user.t_delete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    valid_password = user_login_service.validate_password(request_payload, existing_user)
    if not valid_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    access_token = user_login_service.generate_access_token(existing_user)
    return {"message": "Login successful", "access_token": access_token}


@auth_router.post(
    "/password-recovery/{email}",
    description="This API endpoint allows users to ask for password reset via email.",
    status_code=status.HTTP_200_OK,
    response_model=MsgSchema,
    responses={
        404: {
            "description": "The user with this email does not exist in the system.",
            "content": {
                "application/json": {"example": {
                    "detail": "The user with this email does not exist in the system."
                }}
            },
        }
    }
)
async def recover_password(
        email: str,
        db: Session = Depends(get_db)
) -> Any:
    user = user_login_db_handler.get_by_column(
        db=db, column_name='email', value=email
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this email does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    await send_reset_password_email(
        email_to=user.email, token=password_reset_token
    )
    return {"message": "Password recovery email sent"}


@auth_router.post(
    "/reset-password",
    description="This API endpoint allows users to reset their password.",
    status_code=status.HTTP_200_OK,
    response_model=MsgSchema,
    responses={
        400: {
            "description": "Invalid token or Inactive user",
            "content": {"application/json": {"example": {"detail": "Invalid token or Inactive user"}}},
        },
        404: {
            "description": "The user with this email does not exist in the system.",
            "content": {
                "application/json": {"example": {
                    "detail": "The user with this email does not exist in the system."
                }}
            },
        }
    }
)
def reset_password(
        token: str,
        request_payload: ResetPasswordSchema,
        db: Session = Depends(get_db)
) -> Any:
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )
    user = user_login_db_handler.get_by_column(
        db=db, column_name='email', value=email
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this email does not exist in the system.",
        )
    elif user.t_delete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    user_login_service.update_password(
        request_payload=request_payload,
        user=user,
        db=db
    )
    return {"message": "Password updated successfully"}
