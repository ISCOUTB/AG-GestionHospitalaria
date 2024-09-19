from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.api.deps import (
    SessionDep,
    Admin,
    SuperUser
)

from app import models, schemas

router = APIRouter(prefix="/admin")


@router.get("/")
async def root() -> dict:
    return {"detail": "root/admin", "status": status.HTTP_200_OK}


# Get

@router.get("/users")
async def get_all_users(current_user: Admin, db: SessionDep, rol: bool = False, active: bool = True) -> list[schemas.models.UserRoles | schemas.UserAll]:
    """
    Obtiene todos los usuarios dentro del sistema.

    Args:

        rol (bool): Se especifica si se muestra todos los roles del mismo usuario.
            Cuando `rol=True`, entonces la API retorna un objeto del tipo `list[UserAll]` y `UserInfo` cuando `rol=False`.
            Por defecto `rol=False`.

        active (bool): Filtro de solo los usuarios activos dentro del hospital.
            Por defecto `active=True`.
    """
    pass


@router.get("/users/{num_document}")
async def get_user(num_document: str, current_user: Admin, db: SessionDep, active: bool = True) -> schemas.models.UsersInfo | None:
    """
    Obtiene la información básica de un usuario del sistema sin importar el rol 
    
    Args:

        num_document (str): Número de documento del usuario que se desea encontrar.

        active (bool): Filtro de solo los usuarios activos dentro del hospital.
            Por defecto `active=True`.
    """
    pass


@router.get("/doctors")
async def get_all_doctors(current_user: Admin, db: SessionDep, active: bool = True) -> schemas.DoctorAll:
    """
    Obtiene la información de todos los doctores dentro del sistema
    
    Args:

        active (bool): Filtro de solo los doctores activos dentro del hospital.
            Por defecto `active=True`.
    """
    pass


@router.get("/doctors/{num_document}")
async def get_doctor(num_document: str, current_user: Admin, db: SessionDep, active: bool = True) -> schemas.DoctorAll:
    """
    Obtiene la información esencial de un doctor en particular
    
    Args:

        num_document (str): Número de documento del doctor que se desea encontrar.

        active (bool): Filtro de solo los doctores activos dentro del hospital.
            Por defecto `active=True`.
    """
    pass


@router.get("/specialities")
async def get_all_specialities(current_user: Admin, db: SessionDep) -> list[schemas.SpecialityBase]:
    """
    Obtiene todas las especialidades de los doctores activos dentro del hospital
    """
    pass


@router.get("/specialities/{speciality}")
async def get_speciality_doctor(speciality: str, current_user: Admin, db: SessionDep, active: bool = True) -> list[schemas.DoctorAll]:
    """
    Obtiene todos los doctores los cuales tengan una especialidad especifica
    
    Args:

        speciality (str): Nombre de la especialidad por la que se quiere filtrar.

        active (bool): Filtra únicamente por los doctores que estén activos dentro del hospital.
            Por defecto `active=True`
    """
    pass


@router.get("/patients")
async def get_patients(current_user: Admin, db: SessionDep, active: bool = True) -> list[schemas.PatientAll]:
    """
    Obtiene todos los pacientes que están dentro del sistema 
    
    Args:

        active (bool): Filtra únicamente por los usuarios que estén activos dentro del hospital.
            Por defecto `active=True`.
    """
    pass


@router.get("/patients/{num_document}")
async def get_patient(num_document: str, current_user: Admin, db: SessionDep, active: bool = True) -> schemas.PatientAll:
    """
    Obtiene toda la información de un paciente especificando su número de documento

    Args:

        num_document (str): Número de documento del paciente que se desea obtener

        active (bool): Filtra únicamente por todos los pacientes que estén activos en el hospital.
            Por defecto `active=True`.
    """
    pass


@router.get("/stats", summary="Get Statistics About Hospital")
async def get_stats(current_user: Admin, db: SessionDep) -> list[float, float, float]:
    """
    Obtiene los indicadores estadísiticos del hospital.

    Los indicadores estadísitcos del hospital están listados de la siguiente manera:  
        1. Porcentaje de ocupación hospitalaria.  
        2. Promedios de estancia de los pacientes en el hospital.  
        3. Cantidad de admisiones y altas por día.  
    """
    pass


@router.get("/beds", summary="Get Number All Beds")
async def get_beds(current_user: Admin, db: SessionDep) -> int:
    """
    Obtiene la cantidad de camas totales en el hospital
    """
    pass


# Post

@router.post("/")
async def create_admin(current_user: SuperUser, db: SessionDep, new_admin: schemas.UserCreate) -> schemas.models.UserRoles:
    """
    Crea un nuevo administrador en el sistema. Esta operación es únicamente reservada para el super usuario del sistema

    Args:  
        new_admin (UserCreate): Información esencial del nuevo administrador  
    """
    pass


@router.post("/doctors/{num_document}", summary="Add Doctor Specialities")
async def create_doctor(num_document: str,
                        current_user: Admin,
                        db: SessionDep,
                        specialities: list[schemas.SpecialityBase]) -> schemas.DoctorAll:
    """
    Agrega las especialidades dado el número documento del doctor. Antes de agregar las especialidades, la información 
    esencial del doctor tuvo que haber sido previamente creada. 

    Args:  
        num_document (str): Número de documento del doctor  
        specialities (list[SpecialityBase]): Lista con el nombre de las especialidades que se le agregarán al doctor.  
    """
    pass


@router.post("/beds/")
async def add_bed(current_user: Admin, db: SessionDep, room: schemas.BedBase) -> schemas.models.Beds:
    """
    Agrega una nueva cama al hospital al hospital especificando el cuarto
    """
    pass


# Update

@router.put("/users/{num_document}")
async def update_user(num_document: str, current_user: Admin, db: SessionDep, updated_info: schemas.UserBase) -> schemas.models.UsersInfo:
    """
    Actualiza la información completa de cualquier usuario dentro del sistema que no sea un administrador.

    Args:  
        num_document (str): Número de documento del usuario a modifical  
        updated_info (UserUpdate): Información que se quiere actualizar.  
    """
    pass


@router.put("/{num_document}")
async def update_admin(num_document: str, current_user: SuperUser, db: SessionDep, updated_info) -> schemas.models.UsersInfo:
    """
    Actualiza la información completa de cualquier usuario, incluyendo administradores
    """
    pass


@router.put("/patient/{num_document}")
async def update_patient(num_document: str, current_user: Admin, db: SessionDep, updated_info: schemas.ResponsablesInfo) -> schemas.models.PatientInfo:
    """ 
    Actualiza la información del responsable dado un determinado paciente
    """
    pass


# Delete

@router.delete("/users/{num_document}/{rol}")
async def delete_user(num_document: str, rol: Literal["doctor", "patient"], current_user: Admin, db: SessionDep) -> schemas.User:
    """
    "Elimina" a un usuario dentro del sistema. En realidad, lo que se hace es colocar al usuario como inactivo


    Args:  
        num_document (str): Número de documento del usuario que se va a "eliminar".  
        rol (Literal["doctor", "patient"]): Se especifica el rol el cual se va a "eliminar". Únicamente puede ser doctores o pacientes.  
    """
    pass


@router.delete("/{num_document}")
async def delete_admin(num_document: str, current_user: SuperUser, db: SessionDep) -> schemas.User:
    """
    "Elimina" o coloca como inactivo a un administrador dentro del sistema. Esta es una operación que está reservada únicamente para un
    solo administrador, el cual es llamado el SuperUsuario.

    Args:

        num_document (str): Número del documento de administrador que se va a "eliminar".
    """
    pass


@router.delete("/doctors/{num_document}")
async def delete_speciality(num_document: str, current_user: Admin, db: SessionDep, speciality: schemas.SpecialityBase) -> schemas.DoctorAll:
    """
    Elimina la especialidad de un doctor especificando su número de documento.

    Args:

        num_document (str): Número del documento del doctor

        speciality (SpecialityBase): Especialidad del doctor que se quiere eliminar
    """
    pass


@router.delete("/beds/{room}")
async def delete_bed(room: str, current_user: Admin, db: SessionDep) -> schemas.models.Beds:
    """
    Elimina una cama dentro del hospital que no esté en uso, especificando el cuarto donde esté
    """
    pass
