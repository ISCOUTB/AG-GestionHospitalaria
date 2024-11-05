from time import perf_counter
from typing import Literal

from fastapi import APIRouter, status, Request
from fastapi.responses import FileResponse

from app.api.deps import SessionDep, Patient, NonPatient, Admin, log_request

from app import schemas
from app.api import exceptions
from app.crud import crud_patient, crud_document

router = APIRouter(prefix="/patients")


@router.get("/documents")
async def get_documents(request: Request, current_user: Patient) -> schemas.AllFiles:
    """
    Devuelve todos los documentos asociados del paciente
    """
    start_time = perf_counter()
    documents = crud_document.get_documents(current_user.num_document)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return documents


@router.get("/documents/{filename}")
async def download_document(
    filename: str, request: Request, current_user: Patient, kind: Literal["0", "1", "2"]
) -> FileResponse:
    """
    Descarga el archivo deseado por el paciente
    """
    start_time = perf_counter()
    kind = int(kind)
    file = crud_document.get_file(current_user.num_document, filename, kind)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return file


@router.get("/responsable")
async def get_patient_info(
    request: Request, current_user: Patient, db: SessionDep
) -> schemas.PatientAll:
    """
    Devuelve toda la información del paciente, incluyendo la de los responsables
    """
    start_time = perf_counter()
    patient = crud_patient.get_patient(current_user.num_document, db)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    if patient is None:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.patient_not_found

    await log_request(request, status.HTTP_200_OK, *log_data)
    return patient


@router.get("/")
async def get_patients(
    request: Request, current_user: Admin, db: SessionDep, active: bool = True
) -> list[schemas.PatientAll]:
    """
    Obtiene todos los pacientes que están dentro del sistema
    """
    start_time = perf_counter()
    patients = crud_patient.get_patients(db, active)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return patients


@router.get("/{num_document}")
async def get_patient(
    num_document: str,
    request: Request,
    current_user: NonPatient,
    db: SessionDep,
    active: bool = True,
) -> schemas.PatientAll:
    """
    Obtiene toda la información de un paciente especificando su número de documento
    """
    start_time = perf_counter()
    patient = crud_patient.get_patient(num_document, db, active)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    if patient is None:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.patient_not_found

    await log_request(request, status.HTTP_200_OK, *log_data)
    return patient


@router.post("/{num_document}", status_code=status.HTTP_201_CREATED)
async def add_responsable(
    num_document: str,
    request: Request,
    current_user: NonPatient,
    db: SessionDep,
    responsable_info: schemas.ResponsablesInfo,
) -> schemas.ApiResponse:
    """
    Agrega información del responsable de un paciente
    """
    start_time = perf_counter()
    out = crud_patient.add_responsable(num_document, responsable_info, db)
    process_time = perf_counter() - start_time

    body = responsable_info.model_dump()
    log_data = [process_time, body, current_user.num_document, current_user.rol]
    if out == 1:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.patient_not_found

    if out == 2:
        await log_request(request, status.HTTP_400_BAD_REQUEST, *log_data)
        raise exceptions.patient_cannot_be_his_responsable

    if out == 3:
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.patient_cannot_be_responsable

    if out == 4:
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.responsable_found

    await log_request(request, status.HTTP_201_CREATED, *log_data)
    return schemas.ApiResponse(detail="Información del responsable agregada")


@router.put("/{num_document}")
async def update_responsable(
    num_document: str,
    request: Request,
    current_user: NonPatient,
    db: SessionDep,
    updated_info: schemas.ResponsablesInfo,
) -> schemas.ApiResponse:
    """
    Actualiza la información del responsable dado un determinado paciente
    """
    start_time = perf_counter()
    out = crud_patient.update_patient(num_document, updated_info, db)
    process_time = perf_counter() - start_time

    body = updated_info.model_dump()
    log_data = [process_time, body, current_user.num_document, current_user.rol]
    if out == 1:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.patient_not_found

    if out == 2:
        await log_request(request, status.HTTP_400_BAD_REQUEST, *log_data)
        raise exceptions.patient_cannot_be_his_responsable

    if out == 3:
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.patient_cannot_be_responsable

    if out == 4:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.responsable_not_found

    await log_request(request, status.HTTP_200_OK, *log_data)
    return schemas.ApiResponse(detail="Información del responsable actualizada")


@router.delete("/{num_document}")
async def delete_responsable(
    num_document: str, request: Request, current_user: NonPatient, db: SessionDep
) -> schemas.ApiResponse:
    """
    Elimina la información del responsable de un paciente
    """
    start_time = perf_counter()
    out = crud_patient.delete_responsable(num_document, db)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    if out == 1:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.patient_not_found

    if out == 2:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.responsable_not_found

    await log_request(request, status.HTTP_200_OK, *log_data)
    return schemas.ApiResponse(detail="Información del responsable eliminada")
