from typing import Literal

from fastapi import APIRouter, HTTPException, status

from app.api.deps import (
    SessionDep,
    Admin,
    SuperUser
)

from app import schemas
from app.crud import *

router = APIRouter(prefix="/beds")


@router.get("/")
async def root() -> dict:
    return {"detail": "root/beds", "status": status.HTTP_200_OK}


@router.get("/beds", summary="Get Number All Beds")
async def get_beds(current_user: Admin, db: SessionDep, all: bool = False) -> list[schemas.models.Beds] | list[schemas.BedAll]:
    """
    Obtiene un listado con todas las camas del hospital
    """
    return crud_bed.get_beds(db, all)


@router.post("/beds/")
async def add_bed(current_user: Admin, db: SessionDep, bed_info: schemas.BedBase) -> dict:
    """
    Agrega una nueva cama al hospital al hospital especificando el cuarto
    """
    out = crud_bed.add_bed(bed_info, db)

    if out == 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Cama en el cuarto ya especificado')
    
    return {'status': status.HTTP_201_CREATED, 'detail': 'Cama agregada perfectamente'}


@router.delete("/beds/{room}")
async def delete_bed(room: str, current_user: Admin, db: SessionDep) -> schemas.models.Beds:
    """
    Elimina una cama dentro del hospital que no esté en uso, especificando el cuarto donde esté
    """
    out = crud_bed.delete_bed(room, db)

    if out == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Cama no encontrada')
    
    if out == 2:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Cama en uso')
    
    return {'status': status.HTTP_200_OK, 'detail': 'Cama eliminada de la habitación'}
