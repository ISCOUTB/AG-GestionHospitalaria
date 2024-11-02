import os

from fastapi import APIRouter, status, File, UploadFile
from fastapi.responses import FileResponse

from app.api.deps import Admin, Doctor
from app.api import exceptions

from app.core.config import settings
from app.crud import crud_document

from app import schemas

router = APIRouter(prefix="/documents")


@router.get("/all/{num_document}")
async def get_all_documents(
    num_document: str, current_user: Doctor, 
) -> schemas.AllFiles:
    """
    Obtiene todos los documentos asociados a un paciente
    """
    return crud_document.get_documents(num_document)


@router.get("/all/")
async def get_all(current_user: Doctor, ) -> list[schemas.AllFiles]:
    """
    Obtiene todos los documentos de todos los pacientes en un archivo .zip
    """
    documents: list[schemas.AllFiles] = []
    for num_document in os.listdir(settings.PATIENT_DOCS_PATH):
        documents.append(crud_document.get_documents(num_document))
    
    return documents


@router.get("/histories/{num_document}", summary="Get Clinical History")
async def get_history(num_document: str, current_user: Doctor) -> FileResponse:
    """
    Obtiene la historia clínica de un determinado paciente en un archivo .txt
    """
    return crud_document.get_file(num_document, settings.HISTORY_FILENAME)


@router.get("/histories", summary="Get Clinical Histories")
async def get_histories(current_user: Doctor, ) -> list[str]:
    """
    Obtiene todas las historias clínicas de todos los pacientes
    """
    return crud_document.get_histories()


@router.get("/orders/{num_document}")
async def get_order(num_document: str, current_user: Doctor) -> list[str]:
    """
    Obtiene todas las órdenes médicas de un determinado paciente
    """
    return crud_document.get_files(num_document, 0)


@router.get("/orders/{num_document}/{filename}")
async def get_order(num_document: str, filename: str, current_user: Doctor) -> FileResponse:
    """
    Obtiene un archivo de una orden médica de un determinado paciente
    """
    return crud_document.get_file(num_document, filename, 1)


@router.get("/results/{num_document}")
async def get_result(num_document: str, current_user: Doctor) -> list[str]:
    """
    Obtiene todos los resultados de los examenes médicos para un determinado paciente
    """
    return crud_document.get_files(num_document, 1)


@router.get("/results/{num_document}/{filename}")
async def get_result(num_document: str, filename: str, current_user: Doctor) -> FileResponse:
    """
    Obtiene un archivo de un resultado médico de un determinado paciente
    """
    return crud_document.get_file(num_document, filename, 2)


@router.put("/histories/{num_document}", summary="Update Clinical History")
async def update_history(num_document: str, current_user: Doctor, history: UploadFile = File(...)) -> dict:
    """
    Actualiza la historia clínica de un determinado paciente
    """
    out = crud_document.update_history(num_document, history)

    if out == 1:
        raise exceptions.failed_to_save_historial
    if out == 2:
        raise exceptions.failed_to_save_history
    
    return {"status": status.HTTP_200_OK, "detail": "Historia clínica actualizada correctamente"}


@router.post("/{num_document}")
async def add_file(
    num_document: str,
    kind: schemas.kind_files,
    current_user: Doctor,
    file: UploadFile = File(...),
) -> dict:
    """
    Agrega un documento médico (ya sea orden o resultados de un examen) a un determinado paciente
    """
    out = crud_document.add_file(num_document, kind, file)
    if out == 1:
        raise exceptions.failed_to_save_order
    
    return {"status": status.HTTP_201_CREATED, "detail": "Archivo agregado correctamente"}

@router.delete("/results/{num_document}")
async def delete_file(
    num_document: str, filename: str, current_user: Admin, kind: schemas.kind_files
):
    """
    Elimina un archivo médico de un determinado paciente (no incluye la historia clínica)
    """
    out = crud_document.delete_file(num_document, filename, kind)
    if out == 1:
        raise exceptions.failed_to_found_file
    if out == 2:
        raise exceptions.failed_to_delete_file
    
    return {"status": status.HTTP_200_OK, "detail": "Archivo eliminado correctamente"}
