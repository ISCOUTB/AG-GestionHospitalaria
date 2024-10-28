from typing import Literal

from fastapi import APIRouter, status, File, UploadFile
from fastapi.responses import FileResponse

from app.api.deps import SessionDep, Admin, Doctor


router = APIRouter(prefix="/documents")


# GET


@router.get("/")
async def root() -> dict:
    return {"detail": "root/documents", "status": status.HTTP_200_OK}


@router.get("/all/{num_document}")
async def get_all_documents(
    num_document: str, current_user: Doctor, db: SessionDep
) -> FileResponse:
    """
    Obtiene todos los documentos asociados a un paciente en un archivo .zip
    """
    pass


@router.get("/all")
async def get_all(current_user: Doctor, db: SessionDep) -> FileResponse:
    """
    Obtiene todos los documentos de todos los pacientes en un archivo .zip
    """


@router.get("/histories/{num_document}", summary="Get Clinical History")
async def get_history(
    num_document: str, current_user: Doctor, db: SessionDep
) -> FileResponse:
    """
    Obtiene la historia clínica de un determinado paciente en un archivo .txt
    """
    pass


@router.get("/histories", summary="Get Clinical Histories")
async def get_histories(current_user: Doctor, db: SessionDep) -> FileResponse:
    """
    Obtiene todas las historias clínicas de todos los pacientes en un archivo .zip
    """


@router.get("/orders/{num_document}")
async def get_order(
    num_document: str, current_user: Doctor, db: SessionDep
) -> FileResponse:
    """
    Obtiene todas las órdenes médicas de un determinado paciente en un archivo .zip
    """
    pass


@router.get("/orders")
async def get_orders(current_user: Doctor, db: SessionDep) -> FileResponse:
    """
    Obtiene todas las órdenes médicas de todos los pacientes en un archivo .zip
    """
    pass


@router.get("/results/{num_document}")
async def get_result(
    num_document: str, current_user: Doctor, db: SessionDep
) -> FileResponse:
    """
    Obtiene todos los resultados de los examenes médicos para un determinado paciente en un archivo .zip
    """
    pass


@router.get("/results")
async def get_results(current_user: Doctor, db: SessionDep) -> FileResponse:
    """
    Obtiene todos los resultados de los examanes médicos de todos los pacientes en un archivo .zip
    """
    pass


# UPDATE


@router.put("/histories/{num_document}", summary="Update Clinical History")
async def update_history(num_document: str, current_user: Doctor, db: SessionDep):
    """
    Actualiza la historia clínica de un determinado paciente
    """
    pass


# POST


@router.post("/{num_document}")
async def add_order(
    num_document: str,
    type: Literal["orders", "results"],
    current_user: Doctor,
    db: SessionDep,
    file: UploadFile = File(...),
) -> FileResponse:
    """
    Agrega un documento médico (ya sea orden o resultados de un examen) a un determinado paciente
    """
    pass


# DELETE


@router.delete("/results/{num_document}")
async def delete_file(
    num_document: str, filename: str, current_user: Admin, db: SessionDep
):
    """
    Elimina un archivo médico de un determinado paciente (no incluye la historia clínica)
    """
    pass
