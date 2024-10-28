from datetime import date
from pydantic import BaseModel


class BaseAppointment(BaseModel):
    """
    Modelo de datos base válido para registar una hospitalización y una consulta médica

    Attributes:
        num_doc_patient (str): Número de documento del paciente.
        num_doc_doctor (str): Número de documento del doctor.
    """

    num_doc_patient: str
    num_doc_doctor: str


class Consultation(BaseAppointment):
    """
    Modelo de datos para representar una consulta médica.

    Inherits from:
        BaseAppointment: Contiene los atributos comunes para registrar una consulta médica

    Attributes:
        area (str): Área donde se realiza la consulta.
        day (datetime.date): Fecha de la consulta, por defecto la fecha actual.
    """

    area: str
    day: date = date.today()


class RegisterHospitalization(BaseAppointment):
    """
    Modelo de datos para registrar la hospitalización de un paciente.

    Inherits from:
        BaseAppointment: Contiene los atributos comunes para registrar una consulta médica

    Attributes:
        room (str): Cuarto donde estará el paciente hospitalizado
        entry_day (datetime.date): Fecha de ingreso al hospital, por defecto la fecha actual.
    """

    room: str
    entry_day: date = date.today()


class DischargeHospitalization(BaseModel):
    """
    Modelo de datos para registrar el alta hospitalaria de un paciente.

    Attributes:
        last_day (datetime.date): Último día de hospitalización, por defecto la fecha actual.
    """

    last_day: date = date.today()


class Hospitalization(BaseAppointment):
    """
    Modelo de datos para obtener una hospitalización.

    Inherits from:
        BaseAppointment: Contiene los atributos comunes para registrar una hospitalización

    Attributes:
        entry_day (datetime.date): Fecha de ingreso al hospital.
        last_day (datetime.date | None): Última fecha del paciente en el hospital. Si `last_day=None`,
            significa que aún no ha sido dado de alta el paciente.
    """

    entry_day: date
    last_day: date | None = None
