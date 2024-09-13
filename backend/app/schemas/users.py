import datetime
from pydantic import BaseModel
from typing import Literal

Roles = Literal["admin", "doctor", "patient"]


class UserInfo(BaseModel):
    number_document: str
    rol: Roles
    type_document: str | None = None
    name: str | None = None
    surname: str | None = None
    sex: str | None = None
    birthday: datetime.date | None = None
    address: str | None = None
    phone: str | None = None


class UserLogin(BaseModel):
    """ Información para acceder al sistema """
    number_document: str
    password: str
    rol: Roles


class UserUpdate(BaseModel):
    """ Información modificable general de los usuarios """
    number_document: str  # Solo se pide para ubicar al usuario, no se va a actualizar
    password: str | None = None
    address: str | None = None
    phone: str | None = None


class UserSearch(BaseModel):
    number_document: str
    rol: Roles
