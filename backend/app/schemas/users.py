import datetime
from pydantic import BaseModel
from typing import Literal

Roles = Literal["admin", "doctor", "patient"]


class UserBase(BaseModel):
    """
    Clase base que contiene los atributos comunes de un usuario.

    Attributes:
        num_document (str): Número de documento de identificación del usuario.
        type_document (str | None): Tipo de documento (opcional).
        name (str | None): Nombre del usuario (opcional).
        surname (str | None): Apellido del usuario (opcional).
        sex (str | None): Sexo del usuario (opcional).
        birthday (datetime.date | None): Fecha de nacimiento del usuario (opcional).
        address (str | None): Dirección del usuario (opcional).
        phone (str | None): Teléfono del usuario (opcional).
        email (str | None): Email del usuario (opcional).
    """

    num_document: str
    type_document: str | None = None
    name: str | None = None
    surname: str | None = None
    sex: str | None = None
    birthday: datetime.date | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None


class User(UserBase):
    """
    Modelo de usuario con información para un rol específico.

    Inherits from:
        UserBase: Contiene los atributos comunes de un usuario.

    Attributes:
        rol (Roles): Rol del usuario, que debe ser uno de los valores de 'Roles'.
    """

    rol: Roles


class UserAll(UserBase):
    """
    Modelo que extiende UserBase para representar un usuario con todos sus roles.

    Inherits from:
        UserBase: Contiene los atributos comunes de un usuario.

    Attributes:
        roles (list[tuple[Roles, bool]]): Lista de roles asociados al usuario junto a su
            estado actual en cada rol.
    """

    roles: list[tuple[Roles, bool]]


class UserLogin(BaseModel):
    """
    Modelo de datos para el inicio de sesión de un usuario.

    Attributes:
        num_document (str): Número de documento de identificación del usuario.
        password (str): Contraseña para el acceso del usuario.
        rol (Roles): Rol del usuario al que se autentica.
    """

    num_document: str
    password: str
    rol: Roles


class UserUpdate(BaseModel):
    """
    Modelo para la actualización de datos de un usuario.

    Attributes:
        password (str | None): Nueva contraseña (opcional).
        address (str | None): Nueva dirección (opcional).
        phone (str | None): Nuevo número de teléfono (opcional).
        email (str | None): Nuevo email (opcional)
    """

    password: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None


class UserUpdateAll(UserUpdate):
    """
    Modelo para actualizar los datos completos de un usuario

    Inherits from:
        UserUpdate: Contiene los atributos comunes para actualizar información de un usuario

    Attributes:
        num_document (str | None): Nuevo número de documento de identificación del usuario (opcional).
        type_document (str | None): Nuevo tipo de documento (opcional).
        name (str | None): Nuevo nombre del usuario (opcional).
        surname (str | None): Nuevo apellido del usuario (opcional).
        sex (str | None): Nuevo sexo del usuario (opcional).
        birthday (datetime.date | None): Nueva fecha de nacimiento del usuario (opcional).
    """

    num_document: str | None = None
    type_document: str | None = None
    name: str | None = None
    surname: str | None = None
    sex: str | None = None
    birthday: datetime.date | None = None


class UserSearch(BaseModel):
    """
    Modelo para buscar un usuario en el sistema.

    Attributes:
        num_document (str): Número de documento del usuario.
        rol (Roles): Rol del usuario que se está buscando.
    """

    num_document: str
    rol: Roles


class UserCreate(User):
    """
    Modelo para crear un usuario en el sistema

    Inherits from:
        User: Contiene los atributos comunes de un usuario.

    Attributes:
        password (str): Contraseña del nuevo usuario
    """

    password: str
