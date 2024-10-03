from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.api.deps import (
    SessionDep,
    Patient,
    Admin
)

from app import schemas
from app.crud import *

router = APIRouter(prefix="/patients")


@router.get("/")
async def root() -> dict:
    return {"detail": "root/patient", "status": status.HTTP_200_OK}


@router.get("/documents")
async def get_documents(current_user: Patient, db: SessionDep) -> FileResponse:
    """
    Devuelve todos los documentos asociados a un determinado paciente en un archivo zip
    """
    pass


@router.get("/responsable")
async def get_responsables(current_user: Patient, db: SessionDep) -> schemas.PatientAll:
    """
    Devuelve toda la información del paciente, incluyendo la de los responsables
    """
    pass


@router.get("/all")
async def get_patients(current_user: Admin, db: SessionDep, active: bool = True) -> list[schemas.PatientAll]:
    """
    Obtiene todos los pacientes que están dentro del sistema 
    """
    return crud_patient.get_patients(db, active)


@router.get("/{num_document}")
async def get_patient(num_document: str, current_user: Admin, db: SessionDep, active: bool = True) -> schemas.PatientAll:
    """
    Obtiene toda la información de un paciente especificando su número de documento
    """
    patient = crud_patient.get_patient(num_document, db, active)
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Paciente no encontrado')

    return patient


@router.put("/{num_document}")
async def update_patient(num_document: str, current_user: Admin, db: SessionDep, updated_info: schemas.ResponsablesInfo) -> dict:
    """ 
    Actualiza la información del responsable dado un determinado paciente
    """
    out = crud_patient.update_patient(num_document, updated_info, db)

    if out == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Paciente no encontrado')
    
    if out == 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Paciente no puede ser su propio responsable')

    if out == 3:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Responsable no puede ser un paciente activo en el hospital')

    if out == 4:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Información previa del responsable no existente')
    
    return {'status': status.HTTP_200_OK, 'detail': 'Información del responsable actualizada'}
