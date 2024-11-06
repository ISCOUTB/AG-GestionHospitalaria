import datetime

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import BaseModel


class DoctorSpecialities(BaseModel):
    __tablename__ = "doctor_specialities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    speciality_id = Column(Integer, ForeignKey("specialities.id"), nullable=False)

    specialities = relationship(
        "Specialities",
        uselist=True,
        back_populates="doctor_specialities",
        passive_deletes=True,
        passive_updates=True,
    )
    user_roles = relationship(
        "UserRoles",
        uselist=True,
        back_populates="doctor_specialities",
        passive_deletes=True,
        passive_updates=True,
    )
