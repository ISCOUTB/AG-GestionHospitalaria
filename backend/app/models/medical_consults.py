import datetime

from sqlalchemy import (
    Column,
    Date,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.core.db import BaseModel


class MedicalConsults(BaseModel):
    __tablename__ = "medical_consults"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_patient = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    id_doctor = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    area = Column(String, nullable=False)
    day = Column(Date, default=datetime.date.today(), nullable=False)

    patient = relationship(
        "UserRoles",
        uselist=True,
        foreign_keys=[id_patient],
        back_populates="medical_consults_patient",
        passive_deletes=True,
        passive_updates=True,
    )
    doctor = relationship(
        "UserRoles",
        uselist=True,
        foreign_keys=[id_doctor],
        back_populates="medical_consults_doctor",
        passive_deletes=True,
        passive_updates=True,
    )
