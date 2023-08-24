from sqlalchemy import TIMESTAMP, Column, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID

from backend.models.database import Base


class UserLogin(Base):
    __tablename__ = "user_login"

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    password_salt = Column(String, nullable=False)
    t_create = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    t_update = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=text("now()"),
    )
    t_delete = Column(TIMESTAMP(timezone=True))

    __table_args__ = (UniqueConstraint("email", name="user_login_email_key"),)
