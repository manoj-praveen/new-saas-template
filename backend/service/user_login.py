import uuid
from datetime import timedelta

from sqlalchemy.orm import Session

from backend.db_handler.user_login_handler import user_login_db_handler
from backend.models.user_login import UserLogin
from backend.schemas.user_login import SignUpSchema, ResetPasswordSchema
from backend.utils.utils import generate_salt, hash_password, verify_password, create_access_token


class UserLoginService:

    @staticmethod
    def create_user(request_payload: SignUpSchema, db: Session) -> UserLogin:
        user_data = request_payload.dict()
        user_data['id'] = uuid.uuid4()
        salt = generate_salt()
        password_with_salt = user_data.pop('password') + salt
        user_data['password_hash'] = hash_password(password_with_salt)
        user_data['password_salt'] = salt
        return user_login_db_handler.create(db=db, obj_in=user_data)

    @staticmethod
    def validate_password(request_payload: SignUpSchema, existing_user: UserLogin) -> bool:
        input_password = request_payload.password
        salt = existing_user.password_salt
        return verify_password(password=input_password + salt, hashed_password=existing_user.password_hash)

    @staticmethod
    def update_password(request_payload: ResetPasswordSchema, user: UserLogin, db: Session) -> None:
        request_dict = request_payload.dict()
        password_with_salt = request_dict['new_password'] + user.password_salt
        new_password_hash = hash_password(password_with_salt)
        update_data = {'password_hash': new_password_hash}
        user_login_db_handler.update(db=db, db_obj=user, obj_in=update_data)

    @staticmethod
    def generate_access_token(user: UserLogin) -> str:
        access_token_expires = timedelta(minutes=60)
        return create_access_token(
            data={"email": user.email, "id": str(user.id)}, expires_delta=access_token_expires
        )


user_login_service = UserLoginService()
