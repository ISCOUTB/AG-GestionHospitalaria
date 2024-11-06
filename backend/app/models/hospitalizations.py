import datetime

from sqlalchemy import (
    Column,
    Date,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.core.db import BaseModel


class Hospitalizations(BaseModel):
    __tablename__ = "hospitalizations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_patient = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    id_doctor = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    entry_day = Column(Date, default=datetime.date.today(), nullable=False)
    last_day = Column(Date, default=None, nullable=True)

    patient = relationship(
        "UserRoles",
        uselist=True,
        foreign_keys=[id_patient],
        back_populates="hospitalizations_patient",
        passive_deletes=True,
        passive_updates=True,
    )
    doctor = relationship(
        "UserRoles",
        uselist=True,
        foreign_keys=[id_doctor],
        back_populates="hospitalizations_doctor",
        passive_deletes=True,
        passive_updates=True,
    )
