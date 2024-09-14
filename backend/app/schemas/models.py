# Este archivo contiene únicamente las tablas de app.models únicamente que en PyDantic

import datetime
from app.schemas.users import Roles

from pydantic import BaseModel


class UsersInfo(BaseModel):
    num_document: str
    type_document: str | None = None
    name: str | None = None
    surname: str | None = None
    sex: str | None = None
    birthday: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None

    class Config:
        from_attributes = True


class UserRoles(BaseModel):
    id: int
    num_document: str
    rol: Roles
    password: str
    is_active: bool = True
    inactivity: datetime.date | None = None

    class Config:
        from_attributes = True


class PatientInfo(BaseModel):
    patient_id: int
    num_doc_responsable: str | None = None
    type_doc_responsable: str | None = None
    name_responsable: str | None = None
    surname_responsable: str | None
    phone_responsable: str | None
    relationship_responsable: str | None

    class Config:
        from_attributes = True


class Specialities(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


class DoctorSpecialities(BaseModel):
    id: int
    doctor_id: int
    speciality_id: int

    class Config:
        from_attributes = True


class Beds(BaseModel):
    id: int
    room: str

    class Config:
        from_attributes = True


class BedsUsed(BaseModel):
    id: int
    id_bed: int
    id_patient: int
    id_doctor: int

    class Config:
        from_attributes = True


class MedicalConsults(BaseModel):
    id: int
    id_patient: int
    id_doctor: int
    area: str
    day: datetime.date = datetime.date.today()

    class Config:
        from_attributes = True


class Hospitalizations(BaseModel):
    id: int
    id_patient: int
    id_doctor: int
    entry_day: datetime.date = datetime.date.today()
    last_day: datetime.date | None = None

    class Config:
        from_attributes = True
