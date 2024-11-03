from time import perf_counter

from fastapi import APIRouter, status, Request

from app.api.deps import SessionDep, Admin, log_request

from app import schemas
from app.api import exceptions
from app.crud import crud_doctor

router = APIRouter(prefix="/doctors")


@router.get("/")
async def get_doctors(
    request: Request, current_user: Admin, db: SessionDep, active: bool = True
) -> list[schemas.DoctorAll]:
    """
    Obtiene la información de todos los doctores dentro del sistema
    """
    start_time = perf_counter()
    doctors = crud_doctor.get_doctors(db, active)
    process_time = perf_counter() - start_time
    
    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return doctors


@router.get("/{num_document}")
async def get_doctor(
    request: Request,
    num_document: str,
    current_user: Admin,
    db: SessionDep,
    active: bool = True
) -> schemas.DoctorAll:
    """
    Obtiene la información esencial de un doctor en particular
    """
    start_time = perf_counter()
    doctor = crud_doctor.get_doctor(num_document, db, active)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    if doctor is None:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.doctor_not_found
    
    await log_request(request, status.HTTP_200_OK, *log_data)
    return doctor


@router.get("/specialities")
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


@router.get("/specialities/{speciality}")
async def get_speciality_doctor(
    request: Request,
    speciality: str,
    current_user: Admin,
    db: SessionDep,
    active: bool = True 
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


@router.post("/{num_document}")
async def add_doctor_speciality(
    request: Request,
    num_document: str,
    current_user: Admin,
    db: SessionDep,
    speciality: schemas.Speciality,
) -> dict:
    """
    Agrega una especialidad dado el número documento del doctor. Antes de agregar las especialidades, la información
    esencial del doctor tuvo que haber sido previamente creada. Además, el campo de `description` dentro de `speciality`
    no es necesario de agregar, únicamente cuando la especialidad no esté creada previamente en la base de datos
    """
    body = speciality.model_dump()

    start_time = perf_counter()
    out = crud_doctor.add_doctor_speciality(num_document, db, speciality)
    process_time = perf_counter() - start_time
    log_data = [process_time, body, current_user.num_document, current_user.rol]

    if out == 1:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.doctor_not_found

    if out == 2:
        await log_request(request, status.HTTP_400_BAD_REQUEST, *log_data)
        raise exceptions.create_speciality

    if out == 3:
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.speciality_doctor_found

    await log_request(request, status.HTTP_201_CREATED, *log_data)
    return {
        "detail": "Especialidad agregada al doctor",
        "status": status.HTTP_201_CREATED,
    }


@router.delete("/{num_document}")
async def delete_speciality(
    request: Request,
    num_document: str,
    current_user: Admin,
    db: SessionDep,
    speciality_name: str
) -> dict:
    """
    Elimina la especialidad de un doctor especificando su número de documento.
    """
    start_time = perf_counter()
    speciality = schemas.SpecialityBase(name=speciality_name)
    out = crud_doctor.delete_speciality(num_document, speciality, db)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    if out == 1:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.doctor_not_found

    if out == 2:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.speciality_not_found

    if out == 3:
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.speciality_doctor_not_found

    await log_request(request, status.HTTP_200_OK, *log_data)
    return {"status": status.HTTP_200_OK, "detail": "Especialidad borrada del doctor"}
