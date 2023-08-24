from pydantic import BaseModel, EmailStr, UUID4


class SignUpSchema(BaseModel):
    email: EmailStr
    password: str


class SignUpResponseSchema(BaseModel):
    id: UUID4
    email: EmailStr


class MsgSchema(BaseModel):
    message: str


class SignInResponseSchema(MsgSchema):
    access_token: str


class SignInSchema(SignUpSchema):
    pass


class ResetPasswordSchema(BaseModel):
    new_password: str
