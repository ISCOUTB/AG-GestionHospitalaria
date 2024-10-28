from fastapi import APIRouter, status

from app.api.deps import (
    SessionDep,
    CurrentUser,
    Admin
)

from app import schemas
from app.api import exceptions
from app.crud import crud_user, crud_admin
from app.core.config import settings

router = APIRouter(prefix="/users")


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
        raise exceptions.user_not_found

    return user


@router.get("/")
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
    admins_bool = False
    if current_user.num_document == settings.FIRST_SUPERUSER:
        admins_bool = True

    out = crud_admin.create_user(new_user, db, admins_bool)

    if out == 1:
        raise exceptions.non_superuser

    if out == 2:
        raise exceptions.user_found
    
    return {'status': status.HTTP_201_CREATED, 'detail': 'Usuario creado'}


@router.put("/{num_document}/{rol}")
async def update_user(num_document: str, rol: schemas.Roles,
                      current_user: Admin, db: SessionDep, updated_info: schemas.UserUpdateAll) -> dict:
    """
    Actualiza la información completa de cualquier usuario dentro del sistema que no sea un administrador.
    """
    admins_bool = False
    if current_user.num_document == settings.FIRST_SUPERUSER:
        admins_bool = True

    user_search = schemas.UserSearch(num_document=num_document, rol=rol)
    out = crud_admin.update_user(user_search, updated_info, db, admins_bool)

    if out == 1:
        raise exceptions.user_not_found
    
    if out == 2:
        raise exceptions.non_superuser

    if out == 3:
        raise exceptions.num_document_used
    
    return {'status': status.HTTP_200_OK, 'detail': 'Información del usuario actualizada'}


@router.put("/")
async def update_basic_user(current_user: CurrentUser, db: SessionDep,
                            updated_info: schemas.UserUpdate) -> dict:
    """
    Modifica la información no esencial
    """
    user_search: schemas.UserSearch = schemas.UserSearch(num_document=current_user.num_document,
                                                         rol=current_user.rol)
    out = crud_user.update_basic_info(user_search, updated_info, db)

    if out == 1:
        raise exceptions.user_not_found
    
    return {'status': status.HTTP_200_OK, 'detail': 'Información del usuario actualizada'}


@router.delete("/{num_document}/{rol}")
async def delete_user(num_document: str, rol: schemas.Roles, current_user: Admin, db: SessionDep) -> dict:
    """
    "Elimina" a un usuario activo dentro del sistema. En realidad, lo que se hace es colocar al usuario como inactivo.
    En el caso de los pacientes que están en cama, no se pueden colocar como inactivos todavía.
    """
    admins_bool = False
    if current_user.num_document == settings.FIRST_SUPERUSER:
        admins_bool = True

    user_search: schemas.UserSearch = schemas.UserSearch(num_document=num_document, rol=rol)
    out = crud_admin.delete_user(user_search, db, admins_bool)

    if out == 1:
        raise exceptions.user_not_found
    
    if out == 2:
        raise exceptions.non_superuser
    
    if out == 3:
        raise exceptions.patient_in_bed

    return {'status': status.HTTP_200_OK, 'detail': 'Usuario eliminado'}
