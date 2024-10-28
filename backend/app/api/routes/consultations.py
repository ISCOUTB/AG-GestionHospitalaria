from fastapi import APIRouter, status

from app.api.deps import (
    SessionDep,
    Doctor,
    Admin
)

from app import schemas
from app.crud import crud_consultation
from app.api import exceptions

router = APIRouter(prefix='/consultations')


@router.get("/", tags=["admins"])
async def get_consultations(current_user: Admin, db: SessionDep) -> list[schemas.Consultation]:
    """
    Devuelve una lista con el historial de consultas médicas
    """
    return crud_consultation.get_consultations(db)


@router.post("/")
async def add_consultation(current_user: Doctor,
                           db: SessionDep,
                           consultation_info: schemas.Consultation) -> dict:
    """
    Agrega una nueva consulta médica
    """
    out = crud_consultation.add_consultation(consultation_info, db)

    if out == 1:
        raise exceptions.patient_not_found
    
    if out == 2:
        raise exceptions.doctor_not_found

    return {'status': status.HTTP_201_CREATED, 'detail': 'Consulta médica agregada'}
