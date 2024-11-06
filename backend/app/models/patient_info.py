from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.core.db import BaseModel


class PatientInfo(BaseModel):
    __tablename__ = "patient_info"

    patient_id = Column(Integer, ForeignKey("user_roles.id"), primary_key=True)
    num_doc_responsable = Column(String, default=None, nullable=True)
    type_doc_responsable = Column(String, default=None, nullable=True)
    name_responsable = Column(String, default=None, nullable=True)
    surname_responsable = Column(String, default=None, nullable=True)
    phone_responsable = Column(String, default=None, nullable=True)
    relationship_responsable = Column(String, default=None, nullable=True)

    user_roles = relationship(
        "UserRoles",
        uselist=False,
        back_populates="patient_info",
        passive_deletes=True,
        passive_updates=True,
    )
