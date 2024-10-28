from pydantic import BaseModel
from app.schemas.users import Roles


class TokenPayload(BaseModel):
    """
    Modelo que representa la información contenida en el payload del token.

    Attributes:
        number_document (str): Número de documento del usuario.
        rol (Roles): Rol del usuario asociado al token.
    """

    number_document: str
    rol: Roles


class Token(BaseModel):
    """
    Modelo que representa el token de acceso y su tipo.

    Attributes:
        access_token (str): El token de acceso en sí.
        token_type (str): El tipo de token (generalmente 'bearer').
    """

    access_token: str
    token_type: str
