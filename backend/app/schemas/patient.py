from pydantic import BaseModel
from app.schemas.users import UserBase, Roles


class ResponsablesInfo(BaseModel):
    """
    Modelo para representar la información del responsable de un paciente.

    Attributes:
        num_doc_responsable (str | None): Número de documento del responsable.
        type_doc_responsable (str | None): Tipo de documento del responsable.
        name_responsable (str | None): Nombre del responsable.
        surname_responsable (str | None): Apellido del responsable.
        phone_responsable (str | None): Teléfono del responsable.
        relationship_responsable (str | None): Relación del responsable con el paciente.
    """
    num_doc_responsable: str | None = None
    type_doc_responsable: str | None = None
    name_responsable: str | None = None
    surname_responsable: str | None = None
    phone_responsable: str | None = None
    relationship_responsable: str | None = None


class PatientAll(UserBase, ResponsablesInfo):
    """
    Modelo para representar a un paciente, incluyendo la base de usuario y la información del responsable.

    Inherits from:
        UserBase: Contiene los atributos comunes de un usuario.
        ResponsablesInfo: Contiene la información del responsable del paciente.

    Attributes:
        rol (Roles): El rol del usuario, con valor predeterminado 'patient'.
    """
    rol: Roles = 'patient'
