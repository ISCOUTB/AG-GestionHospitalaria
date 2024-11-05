from time import perf_counter

from fastapi import APIRouter, status, Request

from app.api.deps import SessionDep, Admin, log_request

from app import schemas
from app.crud import crud_doctor

router = APIRouter(prefix="/specialities")


@router.get("/")
async def get_specialities(
    request: Request, current_user: Admin, db: SessionDep
) -> list[schemas.Speciality]:
    """
    Obtiene todas las especialidades de los doctores activos dentro del hospital
    """
    start_time = perf_counter()
    specialities = crud_doctor.get_specialities(db)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return specialities


@router.get("/{speciality}")
async def get_speciality_doctor(
    request: Request,
    speciality: str,
    current_user: Admin,
    db: SessionDep,
    active: bool = True,
) -> list[schemas.DoctorAll]:
    """
    Obtiene todos los doctores los cuales tengan una especialidad especifica
    """
    start_time = perf_counter()
    doctors = crud_doctor.get_speciality_doctor(speciality, db, active)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return doctors
