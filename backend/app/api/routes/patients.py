from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.api.deps import (
    SessionDep,
    Patient
)

from app import models, schemas

router = APIRouter(prefix="/patient")


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
