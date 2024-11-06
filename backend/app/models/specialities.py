from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import BaseModel


class Specialities(BaseModel):
    __tablename__ = "specialities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    doctor_specialities = relationship(
        "DoctorSpecialities",
        uselist=True,
        back_populates="specialities",
        passive_deletes=True,
        passive_updates=True,
    )
