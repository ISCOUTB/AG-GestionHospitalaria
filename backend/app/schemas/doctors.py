from pydantic import BaseModel
from app.schemas.users import UserBase


class SpecialityBase(BaseModel):
    """
    Modelo base que representa una especialidad médica.

    Attributes:
        name (str): Nombre de la especialidad.
    """
    name: str


class Speciality(SpecialityBase):
    """
    Modelo de datos para describir las especialidades

    Inherits from:
        SpecialityBase: Contiene los atributos comunes de una especialidad

    Attributes:
        description (str): Descripción detallada de la especialidad
    """
    description: str | None = None


class DoctorAll(UserBase):
    """
    Modelo que extiende UserBase para representar la información de un doctor.

    Inherits from:
        UserBase: Contiene los atributos comunes de un usuario.

    Attributes:
        specialities (list[SpecialityBase]): Lista de las especialidades del doctor.
    """
    specialities: list[SpecialityBase]
