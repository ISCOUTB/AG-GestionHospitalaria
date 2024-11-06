from sqlalchemy import (
    Column,
    Date,
    Integer,
    String,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.core.db import BaseModel


class UserRoles(BaseModel):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    num_document = Column(String, ForeignKey("users_info.num_document"), nullable=False)
    rol = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    inactivity = Column(Date, default=None, nullable=True)

    __table_args__ = (UniqueConstraint("num_document", "rol", name="unique_users_rol"),)

    users_info = relationship(
        "UsersInfo",
        uselist=True,
        back_populates="user_roles",
        passive_deletes=True,
        passive_updates=True,
    )
    patient_info = relationship(
        "PatientInfo",
        uselist=False,
        back_populates="user_roles",
        passive_deletes=True,
        passive_updates=True,
    )
    doctor_specialities = relationship(
        "DoctorSpecialities",
        uselist=True,
        back_populates="user_roles",
        passive_deletes=True,
        passive_updates=True,
    )

    beds_used_doctor = relationship(
        "BedsUsed",
        uselist=True,
        foreign_keys="BedsUsed.id_doctor",
        back_populates="doctor",
        passive_deletes=True,
        passive_updates=True,
    )
    beds_used_patient = relationship(
        "BedsUsed",
        uselist=False,
        foreign_keys="BedsUsed.id_patient",
        back_populates="patient",
        passive_deletes=True,
        passive_updates=True,
    )

    medical_consults_patient = relationship(
        "MedicalConsults",
        uselist=True,
        foreign_keys="MedicalConsults.id_patient",
        back_populates="patient",
        passive_deletes=True,
        passive_updates=True,
    )
    medical_consults_doctor = relationship(
        "MedicalConsults",
        uselist=True,
        foreign_keys="MedicalConsults.id_doctor",
        back_populates="doctor",
        passive_deletes=True,
        passive_updates=True,
    )

    hospitalizations_patient = relationship(
        "Hospitalizations",
        uselist=True,
        foreign_keys="Hospitalizations.id_patient",
        back_populates="patient",
        passive_deletes=True,
        passive_updates=True,
    )
    hospitalizations_doctor = relationship(
        "Hospitalizations",
        uselist=True,
        foreign_keys="Hospitalizations.id_doctor",
        back_populates="doctor",
        passive_deletes=True,
        passive_updates=True,
    )
