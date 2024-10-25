from typing import Literal

from fastapi import APIRouter, status

from app.api.deps import (
    SessionDep,
    Admin
)

from app import schemas
from app.api import exceptions
from app.crud import crud_bed

router = APIRouter(prefix="/beds")


@router.get("/", summary="Get Number All Beds")
async def get_beds(current_user: Admin, db: SessionDep, all: bool = False) -> list[schemas.models.Beds] | list[schemas.BedAll]:
    """
    Obtiene un listado con todas las camas del hospital
    """
    return crud_bed.get_beds(db, all)


@router.post("/")
async def add_bed(current_user: Admin, db: SessionDep, bed_info: schemas.BedBase) -> dict:
    """
    Agrega una nueva cama al hospital al hospital especificando el cuarto
    """
    out = crud_bed.add_bed(bed_info, db)

    if out == 1:
        raise exceptions.room_already_with_bed
    
    return {'status': status.HTTP_201_CREATED, 'detail': 'Cama agregada perfectamente'}


@router.delete("/{room}")
async def delete_bed(room: str, current_user: Admin, db: SessionDep) -> schemas.models.Beds:
    """
    Elimina una cama dentro del hospital que no esté en uso, especificando el cuarto donde esté
    """
    out = crud_bed.delete_bed(room, db)

    if out == 1:
        raise exceptions.bed_not_found
    
    if out == 2:
        raise exceptions.bed_already_used
    
    return {'status': status.HTTP_200_OK, 'detail': 'Cama eliminada de la habitación'}
