from pydantic import BaseModel


class BedBase(BaseModel):
    """
    Modelo base que representa una cama en un hospital.

    Attributes:
        room (str): Número o nombre de la habitación donde se encuentra la cama.
    """
    room: str


class UseBed(BedBase):
    """
    Modelo para registrar el uso de una cama por un paciente y un doctor.

    Inherits from:
        BedBase: Contiene la información básica sobre la cama.

    Attributes:
        num_doc_doctor (str): Número de documento del doctor que utiliza la cama.
        num_doc_patient (str): Número de documento del paciente que ocupa la cama.
    """
    num_doc_doctor: str
    num_doc_patient: str


class VacateBed(BedBase):
    """
    Modelo para registrar la liberación de una cama.

    Inherits from:
        BedBase: Contiene la información básica sobre la cama.
    """
    pass
