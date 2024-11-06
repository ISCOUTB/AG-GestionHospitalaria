from sqlalchemy import Column, Date, String
from sqlalchemy.orm import relationship

from app.core.db import BaseModel


class UsersInfo(BaseModel):
    __tablename__ = "users_info"

    num_document = Column(String, primary_key=True)
    type_document = Column(String, default=None, nullable=True)
    name = Column(String, default=None, nullable=True)
    surname = Column(String, default=None, nullable=True)
    sex = Column(String(1), default=None, nullable=True)
    birthday = Column(Date, default=None, nullable=True)
    address = Column(String, default=None, nullable=True)
    phone = Column(String, default=None, nullable=True)
    email = Column(String, default=None, nullable=True, unique=True)

    user_roles = relationship(
        "UserRoles",
        uselist=True,
        back_populates="users_info",
        passive_deletes=True,
        passive_updates=True,
    )
