from time import perf_counter

from fastapi import APIRouter, status, Request

from app.api.deps import SessionDep, Doctor, Admin, log_request

from app import schemas
from app.crud import crud_consultation
from app.api import exceptions

router = APIRouter(prefix="/consultations")


@router.get("/", tags=["admins"])
async def get_consultations(
    request: Request, current_user: Admin, db: SessionDep
) -> list[schemas.Consultation]:
    """
    Devuelve una lista con el historial de consultas médicas
    """
    start_time = perf_counter()
    consultations = crud_consultation.get_consultations(db)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return consultations


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_consultation(
    request: Request,
    current_user: Doctor,
    db: SessionDep,
    consultation_info: schemas.Consultation,
) -> schemas.ApiResponse:
    """
    Agrega una nueva consulta médica
    """
    body = consultation_info.model_dump()
    start_time = perf_counter()
    out = crud_consultation.add_consultation(consultation_info, db)
    process_time = perf_counter() - start_time

    log_data = [process_time, body, current_user.num_document, current_user.rol]
    if out == 1:
        process_time = perf_counter() - start_time
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.patient_not_found

    if out == 2:
        process_time = perf_counter() - start_time
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.doctor_not_found
    
    if out == 3:
        process_time = perf_counter() - start_time
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.patient_doctor_same_document

    process_time = perf_counter() - start_time
    await log_request(request, status.HTTP_201_CREATED, *log_data)
    return schemas.ApiResponse(detail="Consulta médica agregada")
