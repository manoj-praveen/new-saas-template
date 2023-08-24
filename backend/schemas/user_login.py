from pydantic import UUID4, BaseModel, EmailStr


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
