from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.api.deps import (
    SessionDep,
    Admin
)

from app import schemas
from app.crud import *

router = APIRouter(prefix="/doctors")


@router.get("/")
async def root() -> dict:
    return {"detail": "root/doctor", "status": status.HTTP_200_OK}


@router.get("/all")
async def get_doctors(current_user: Admin, db: SessionDep, active: bool = True) -> list[schemas.DoctorAll]:
    """
    Obtiene la información de todos los doctores dentro del sistema
    """
    return crud_doctor.get_all_doctors(db, active)


@router.get("/{num_document}")
async def get_doctor(num_document: str, current_user: Admin, db: SessionDep, active: bool = True) -> schemas.DoctorAll:
    """
    Obtiene la información esencial de un doctor en particular
    """
    doctor = crud_doctor.get_doctor(num_document, db, active)

    if doctor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Doctor no encontrado')

    return doctor


@router.get("/specialities")
async def get_specialities(current_user: Admin, db: SessionDep) -> list[schemas.Speciality]:
    """
    Obtiene todas las especialidades de los doctores activos dentro del hospital
    """
    return crud_doctor.get_specialities(db)


@router.get("/specialities/{speciality}")
async def get_speciality_doctor(speciality: str, current_user: Admin, db: SessionDep, active: bool = True) -> list[schemas.DoctorAll]:
    """
    Obtiene todos los doctores los cuales tengan una especialidad especifica
    """
    return crud_doctor.get_speciality_doctor(speciality, db, active)


@router.post("/doctors/{num_document}")
async def add_doctor_speciality(num_document: str, current_user: Admin,
                        db: SessionDep, speciality: schemas.Speciality) -> dict:
    """
    Agrega una especialidad dado el número documento del doctor. Antes de agregar las especialidades, la información 
    esencial del doctor tuvo que haber sido previamente creada. Además, el campo de `description` dentro de `speciality`
    no es necesario de agregar, únicamente cuando la especialidad no esté creada previamente en la base de datos
    """
    out = crud_doctor.add_doctor_speciality(num_document, db, speciality)

    if out == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Doctor no encontrado')
    
    if out == 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Especialidad no encontrada. Provea una descripción para crearla')

    if out == 3:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Relación existente entre el doctor y la especialidad')

    return {'detail': 'Especialidad agregada al doctor', 'status': status.HTTP_201_CREATED}


@router.delete("/{num_document}")
async def delete_speciality(num_document: str, current_user: Admin, db: SessionDep,
                            speciality: schemas.SpecialityBase) -> schemas.DoctorAll:
    """
    Elimina la especialidad de un doctor especificando su número de documento.
    """
    out = crud_doctor.delete_speciality(num_document, speciality, db)

    if out == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Doctor no encontrado')

    if out == 2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Especialidad no encontrada')
    
    if out == 3:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Relación entre doctor y especialidad no existente')

    return {'status': status.HTTP_200_OK, 'detail': 'Especialidad borrada del doctor'}
