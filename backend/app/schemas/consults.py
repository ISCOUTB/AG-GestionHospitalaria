from datetime import date
from pydantic import BaseModel


class RegisterConsult(BaseModel):
    """
    Modelo de datos para registrar una consulta médica.

    Attributes:
        id_patient (str): Identificación del paciente.
        id_doctor (str): Identificación del doctor.
        area (str): Área donde se realiza la consulta.
        day (datetime.date): Fecha de la consulta, por defecto la fecha actual.
    """
    id_patient: str
    id_doctor: str
    area: str
    day: date = date.today()


class RegisterHospitalization(BaseModel):
    """
    Modelo de datos para registrar la hospitalización de un paciente.

    Attributes:
        id_patient (str): Identificación del paciente.
        id_doctor (str): Identificación del doctor a cargo.
        entry_day (date): Fecha de ingreso al hospital, por defecto la fecha actual.
    """
    id_patient: str
    id_doctor: str
    entry_day: date = date.today()


class DischargeHospitalization(BaseModel):
    """
    Modelo de datos para registrar el alta hospitalaria de un paciente.

    Attributes:
        id_patient (str): Identificación del paciente.
        last_day (date): Último día de hospitalización, por defecto la fecha actual.
    """
    id_patient: str
    last_day: date = date.today()
