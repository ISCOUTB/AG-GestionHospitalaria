from fastapi import APIRouter, HTTPException, status

from app.api.deps import (
    SessionDep,
    Admin,
    SuperUser
)

from app import schemas
from app.api import exceptions
from app.crud import crud_admin

router = APIRouter(prefix="/admin")


@router.get("/")
async def root() -> dict:
    return {"detail": "root/admin", "status": status.HTTP_200_OK}


@router.get("/stats", summary="Get Statistics About Hospital")
async def get_stats(current_user: Admin, db: SessionDep) -> list[float, float, float]:
    """
    Obtiene los indicadores estadísiticos del hospital.

    Los indicadores estadísitcos del hospital están listados de la siguiente manera:  
        1. Porcentaje de ocupación hospitalaria.  
        2. Promedios de estancia de los pacientes en el hospital.  
        3. Cantidad de admisiones y altas por día.  
    """
    pass


@router.post("/")
async def create_admin(current_user: SuperUser, db: SessionDep, new_admin: schemas.UserCreate) -> dict:
    """
    Crea un nuevo administrador en el sistema. Esta operación es únicamente reservada para el super usuario del sistema
    """
    out = crud_admin.create_user(new_admin, db, True)

    if out == 2:
        raise exceptions.user_found
    
    return {'status': status.HTTP_201_CREATED, 'detail': 'Usuario creado'}


@router.put("/{num_document}")
async def update_admin(num_document: str, current_user: SuperUser, db: SessionDep, updated_info: schemas.UserBase) -> dict:
    """
    Actualiza la información completa de cualquier usuario, incluyendo administradores
    """
    out = crud_admin.update_user(num_document, updated_info, db, True)

    if out == 1:
        raise exceptions.user_not_found
    
    if out == 3:
        raise exceptions.num_document_used
    
    return {'status': status.HTTP_200_OK, 'detail': 'Información del usuario actualizada'}



@router.delete("/{num_document}")
async def delete_admin(num_document: str, current_user: SuperUser, db: SessionDep) -> dict:
    """
    "Elimina" o coloca como inactivo a un administrador dentro del sistema. Esta es una operación que está reservada únicamente para un
    solo administrador, el cual es llamado el SuperUsuario.
    """
    out = crud_admin.delete_user(num_document, 'admin', db, True)

    if out == 1:
        raise exceptions.user_not_found
    
    if out == 3:
        raise exceptions.patient_in_bed

    return {'status': status.HTTP_200_OK, 'detail': 'Usuario eliminado'}
