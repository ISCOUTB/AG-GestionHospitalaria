from fastapi import APIRouter, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse

from app.api.deps import (
    SessionDep,
    Doctor,
    Admin
)

from app import models, schemas

router = APIRouter(prefix="/appointments")


# GET


@router.get("/")
async def root() -> dict:
    return {"detail": "root/appointments", "status": status.HTTP_200_OK}


@router.get("/hospitalizations", tags=["admins"])
async def get_hospitalizations(current_user: Admin, db: SessionDep) -> list[schemas.models.Hospitalizations]:
    """
    Devuelve una lista con el historial de hospitalizaciones
    """
    pass


@router.get("/consultations", tags=["admins"])
async def get_consultations(current_user: Admin, db: SessionDep) -> list[schemas.models.MedicalConsults]:
    """
    Devuelve una lista con el historial de consultas médicas
    """
    pass


# POST


@router.post("/hospitalizations")
async def add_hospitalization(current_user: Doctor,
                              db: SessionDep,
                              hospitalization: schemas.RegisterHospitalization) -> schemas.models.Hospitalizations:
    """
    Agrega una nueva hospitalización
    """
    pass


@router.post("/consultations")
async def add_consultation(current_user: Doctor,
                           db: SessionDep,
                           consultation: schemas.RegisterConsult) -> schemas.models.MedicalConsults:
    """
    Agrega una nueva consulta médica
    """
    pass


# UPDATE

@router.put("/hospitalizations/{id_patient}")
async def discharge_hospitalization(id_patient: str,
                                    current_user: Doctor,
                                    db: SessionDep,
                                    last_day: schemas.DischargeHospitalization) -> schemas.models.Hospitalizations:
    """
    Da el alta a un determinado paciente que esté actualmente hospitalizado
    """
    pass
