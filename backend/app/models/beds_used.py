import datetime

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import BaseModel


class BedsUsed(BaseModel):
    __tablename__ = "beds_used"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_bed = Column(Integer, ForeignKey("beds.id"), unique=True, nullable=False)
    id_patient = Column(
        Integer, ForeignKey("user_roles.id"), unique=True, nullable=False
    )
    id_doctor = Column(Integer, ForeignKey("user_roles.id"), nullable=False)

    beds = relationship(
        "Beds",
        uselist=False,
        back_populates="beds_used",
        passive_deletes=True,
        passive_updates=True,
    )
    patient = relationship(
        "UserRoles",
        uselist=False,
        foreign_keys=[id_patient],
        back_populates="beds_used_patient",
        passive_deletes=True,
        passive_updates=True,
    )
    doctor = relationship(
        "UserRoles",
        uselist=True,
        foreign_keys=[id_doctor],
        back_populates="beds_used_doctor",
        passive_deletes=True,
        passive_updates=True,
    )
