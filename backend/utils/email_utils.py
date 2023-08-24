from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from jinja2 import Environment, FileSystemLoader

from backend.config import get_settings
from backend.utils.utils import PASSWORD_REST_TOKEN_EXPIRY

settings = get_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_USERNAME,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME="System User",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)
SERVER_HOST = settings.SERVER_HOST
EMAIL_TEMPLATES_DIR = settings.EMAIL_TEMPLATES_DIR


async def send_reset_password_email(email_to: str, token: str):
    valid_hours = PASSWORD_REST_TOKEN_EXPIRY / 60
    link = f"{SERVER_HOST}/reset-password?token={token}"
    env = Environment(loader=FileSystemLoader(EMAIL_TEMPLATES_DIR))
    template = env.get_template("reset_password.html")
    formatted_template = template.render(
        email=email_to, link=link, valid_hours=valid_hours
    )
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email_to],
        body=formatted_template,
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
