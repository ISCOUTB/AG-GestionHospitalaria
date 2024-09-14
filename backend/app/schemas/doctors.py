from pydantic import BaseModel
from app.schemas.users import UserBase, Roles


class AddSpeciality(BaseModel):
    """
    Modelo de datos para agregar una especialidad a un doctor.

    Attributes:
        num_document (str): Número de documento del doctor.
        name (str): Nombre de la especialidad a agregar.
        description (str): Descripción detallada de la especialidad.
    """
    num_document: str
    name: str
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
