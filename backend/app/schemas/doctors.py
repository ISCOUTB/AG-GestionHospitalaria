from pydantic import BaseModel
from app.schemas.users import UserBase, Roles


class SpecialityBase(BaseModel):
    """
    Modelo base que representa una especialidad médica.

    Attributes:
        name (str): Nombre de la especialidad.
        description (str): Descripción detallada de la especialidad.
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
    description: str


class DoctorAll(UserBase):
    """
    Modelo que extiende UserBase para representar la información de un doctor.

    Inherits from:
        UserBase: Contiene los atributos comunes de un usuario.

    Attributes:
        rol (Roles): El rol del usuario, con valor predeterminado 'doctor'.
        specialities (list[str]): Lista de nombres de las especialidades del doctor.
    """
    rol: Roles = 'doctor'
    specialities: list[str]
