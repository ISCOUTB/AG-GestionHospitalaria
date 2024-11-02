from time import perf_counter

from fastapi import APIRouter, status, Request

from app.api.deps import SessionDep, Doctor, Admin, log_request

from app import schemas
from app.crud import crud_hospitalization
from app.api import exceptions

router = APIRouter(prefix="/hospitalizations")


@router.get("/", tags=["admins"])
async def get_hospitalizations(
    request: Request,
    current_user: Admin,
    db: SessionDep
) -> list[schemas.Hospitalization]:
    """
    Devuelve una lista con el historial de hospitalizaciones
    """
    start_time = perf_counter()
    hospitalizations = crud_hospitalization.get_hospitalizations(db)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    log_request(request, status.HTTP_200_OK, *log_data)
    return hospitalizations


@router.post("/")
async def add_hospitalization(
    request: Request,
    current_user: Doctor,
    db: SessionDep,
    hospitalization_info: schemas.RegisterHospitalization,
) -> dict:
    """
    Agrega una nueva hospitalización
    """
    start_time = perf_counter()
    out = crud_hospitalization.add_hospitalization(hospitalization_info, db)
    process_time = perf_counter() - start_time

    body = hospitalization_info.model_dump()
    log_data = [process_time, body, current_user.num_document, current_user.rol]
    if out == 1:
        log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.patient_not_found

    if out == 2:
        log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.doctor_not_found

    if out == 3:
        log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.bed_not_found

    if out == 4:
        log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.bed_already_used

    if out == 5:
        log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.patient_already_hospitalized

    log_request(request, status.HTTP_201_CREATED, *log_data)
    return {"status": status.HTTP_201_CREATED, "detail": "Hospitalización agregada"}


@router.put("/{num_doc_patient}")
async def discharge_hospitalization(
    num_doc_patient: str,
    request: Request,
    current_user: Doctor,
    db: SessionDep,
    last_day: schemas.DischargeHospitalization,
) -> dict:
    """
    Da el alta a un determinado paciente que esté actualmente hospitalizado
    """
    start_time = perf_counter()
    out = crud_hospitalization.discharge_hospitalization(num_doc_patient, last_day, db)
    process_time = perf_counter() - start_time

    body = last_day.model_dump()
    log_data = [process_time, body, current_user.num_document, current_user.rol]
    if out == 1:
        log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.patient_not_found

    if out == 2:
        log_request(request, status.HTTP_400_BAD_REQUEST, *log_data)
        raise exceptions.bad_date_formatting

    log_request(request, status.HTTP_200_OK, *log_data)
    return {"status": status.HTTP_200_OK, "detail": "Paciente dado de alta del sistema"}
