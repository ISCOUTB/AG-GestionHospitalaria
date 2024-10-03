from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas import Roles

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(number_document: str, rol: Roles, expires_delta: timedelta) -> str:
    """
    Genera un token de acceso (JWT) para un usuario.

    Args:
        number_document (str): Número de documento del usuario.
        rol (str): Rol del usuario (ej. administrador, doctor).
        expires_delta (datetime.timedelta): Duración del token antes de que expire.

    Returns:
        str: Token JWT generado.
    """
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "number_document": number_document, "rol": rol}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash.

    Args:
        plain_password (str): Contraseña en texto plano a verificar.
        hashed_password (str): Contraseña encriptada (hash) con la que se comparará.

    Returns:
        bool: True si las contraseñas coinciden, False en caso contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera un hash encriptado de una contraseña en texto plano.

    Args:
        password (str): Contraseña en texto plano a encriptar.

    Returns:
        str: Hash encriptado de la contraseña.
    """
    return pwd_context.hash(password)
