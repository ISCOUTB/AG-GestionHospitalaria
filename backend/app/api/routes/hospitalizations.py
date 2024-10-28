from fastapi import APIRouter, status

from app.api.deps import SessionDep, Doctor, Admin

from app import schemas
from app.crud import crud_hospitalization
from app.api import exceptions

router = APIRouter(prefix="/hospitalizations")


@router.get("/", tags=["admins"])
async def get_hospitalizations(
    current_user: Admin, db: SessionDep
) -> list[schemas.Hospitalization]:
    """
    Devuelve una lista con el historial de hospitalizaciones
    """
    return crud_hospitalization.get_hospitalizations(db)


@router.post("/")
async def add_hospitalization(
    current_user: Doctor,
    db: SessionDep,
    hospitalization_info: schemas.RegisterHospitalization,
) -> dict:
    """
    Agrega una nueva hospitalización
    """
    out = crud_hospitalization.add_hospitalization(hospitalization_info, db)

    if out == 1:
        raise exceptions.patient_not_found

    if out == 2:
        raise exceptions.doctor_not_found

    if out == 3:
        raise exceptions.bed_not_found

    if out == 4:
        raise exceptions.bed_already_used

    if out == 5:
        raise exceptions.patient_already_hospitalized

    return {"status": status.HTTP_201_CREATED, "detail": "Hospitalización agregada"}


@router.put("/{num_doc_patient}")
async def discharge_hospitalization(
    num_doc_patient: str,
    current_user: Doctor,
    db: SessionDep,
    last_day: schemas.DischargeHospitalization,
) -> dict:
    """
    Da el alta a un determinado paciente que esté actualmente hospitalizado
    """
    out = crud_hospitalization.discharge_hospitalization(num_doc_patient, last_day, db)

    if out == 1:
        raise exceptions.patient_not_found

    if out == 2:
        raise exceptions.bad_date_formatting

    return {"status": status.HTTP_200_OK, "detail": "Paciente dado de alta del sistema"}
