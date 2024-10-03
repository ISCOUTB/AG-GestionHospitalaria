from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.api.deps import (
    SessionDep,
    CurrentUser,
    Admin
)

from app import schemas
from app.crud import *

router = APIRouter(prefix="/users")


@router.get("/")
async def root() -> dict:
    return {"detail": "root/users", "status": status.HTTP_200_OK}


@router.get("/info")
async def get_info(current_user: CurrentUser, db:SessionDep) -> schemas.UserBase:
    """
    Obtiene toda la información del usuario
    """
    return crud_user.get_user(current_user.num_document, db)


@router.get("/{num_document}")
async def get_user(num_document: str, current_user: Admin, db: SessionDep,
                   rol: bool = False, active: bool = True) -> schemas.UserBase | schemas.UserAll | None:
    """
    Obtiene la información básica de un usuario del sistema sin importar el rol 
    """
    user = crud_user.get_user(num_document, db, rol, active)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Usuario no encontrado')

    return crud_user.get_user(num_document, db, rol, active)


@router.get("/all")
async def get_users(current_user: Admin, db: SessionDep, rol: bool = False,
                    active: bool = True) -> list[schemas.UserBase] | list[schemas.UserAll]:
    """
    Obtiene todos los usuarios dentro del sistema.
    """
    return crud_user.get_users(db, rol, active)


@router.post("/")
async def create_user(current_user: Admin, db: SessionDep, new_user: schemas.UserCreate) -> dict:
    """
    Crea un nuevo usuario dentro en el sistema. No se pueden crear nuevos administradores.
    """
    out = crud_admin.create_user(new_user, db)

    if out == 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='No se pueden crear funciones con este endpoint')

    if out == 2:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Administrador ya registrado en el sistema')
    
    return {'status': status.HTTP_201_CREATED, 'detail': 'Administrador creado'}


@router.put("/{num_document}/{rol}")
async def update_user(num_document: str, rol: schemas.Roles,
                      current_user: Admin, db: SessionDep, updated_info: schemas.UserAll) -> dict:
    """
    Actualiza la información completa de cualquier usuario dentro del sistema que no sea un administrador.
    """
    user_search = schemas.UserSearch(num_document=num_document,
                                                         rol=rol)
    out = crud_admin.update_user(user_search, updated_info, db, False)

    if out == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Usuario no encontrado')
    
    if out == 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='No tienes los permisos para editar a un administrador')

    if out == 3:
        raise HTTPException(status_code=status.HTTP_409_CONFLICTM,
                            detail='Número de documento en uso')
    
    return {'status': status.HTTP_200_OK, 'detail': 'Información del usuario actualizada'}


@router.put("/")
async def update_basic_user(current_user: CurrentUser, db: SessionDep,
                            updated_info: schemas.UserUpdate) -> schemas.models.UsersInfo:
    """
    Modifica la información no esencial de para determinado usuario
    """
    user_search: schemas.UserSearch = schemas.UserSearch(num_document=current_user.num_document,
                                                         rol=current_user.rol)
    out = crud_user.update_basic_info(user_search, updated_info, db)

    if out == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Usuario no encontrado')
    
    return {'status': status.HTTP_200_OK, 'detail': 'Información del usuario actualizada'}


@router.delete("/{num_document}/{rol}")
async def delete_user(num_document: str, rol: Literal["doctor", "patient"], current_user: Admin, db: SessionDep) -> dict:
    """
    "Elimina" a un usuario activo dentro del sistema. En realidad, lo que se hace es colocar al usuario como inactivo.
    En el caso de los pacientes que están en cama, no se pueden colocar como inactivos todavía.
    """
    user_search: schemas.UserSearch = schemas.UserSearch(num_document=num_document, rol=rol)
    out = crud_admin.delete_user(user_search, db, False)

    if out == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Usuario no encontrado')
    
    if out == 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='No tienes los permisos para eliminar a un administrador')
    
    if out == 3:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='No se puede eliminar a un paciente que esté utilizado en una cama')

    return {'status': status.HTTP_200_OK, 'detail': 'Usuario eliminado'}
