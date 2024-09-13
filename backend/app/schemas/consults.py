from datetime import date
from pydantic import BaseModel


class RegisterConsult(BaseModel):
    id_patient: str
    id_doctor: str
    area: str
    day: date = date.today()


class RegisterHospitalization(BaseModel):
    id_patient: str
    id_doctor: str
    entry_day: date = date.today()


class DischargeHospitalization(BaseModel):
    id_patient: str  # Para ubicar al paciente
    last_day: date = date.today()
