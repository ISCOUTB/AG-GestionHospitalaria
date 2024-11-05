from time import perf_counter

from fastapi import APIRouter, status, Request

from app.api.deps import SessionDep, Admin, log_request

from app import schemas
from app.api import exceptions
from app.crud import crud_bed

router = APIRouter(prefix="/beds")


@router.get("/")
async def get_beds(
    request: Request, current_user: Admin, db: SessionDep, all: bool = False
) -> list[schemas.models.Beds] | list[schemas.BedAll]:
    """
    Obtiene un listado con todas las camas del hospital
    """
    start_time = perf_counter()
    beds = crud_bed.get_beds(db, all)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return beds


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_bed(
    request: Request, current_user: Admin, db: SessionDep, bed_info: schemas.BedBase
) -> schemas.ApiResponse:
    """
    Agrega una nueva cama al hospital al hospital especificando el cuarto
    """
    body = bed_info.model_dump()

    start_time = perf_counter()
    out = crud_bed.add_bed(bed_info, db)
    process_time = perf_counter() - start_time

    log_data = [process_time, body, current_user.num_document, current_user.rol]
    if out == 1:
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.room_already_with_bed

    await log_request(request, status.HTTP_201_CREATED, *log_data)
    return schemas.ApiResponse(detail="Cama agregada perfectamente")


@router.delete("/{room}")
async def delete_bed(
    room: str, request: Request, current_user: Admin, db: SessionDep
) -> schemas.ApiResponse:
    """
    Elimina una cama dentro del hospital que no esté en uso, especificando el cuarto donde esté
    """
    start_time = perf_counter()
    out = crud_bed.delete_bed(room, db)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    if out == 1:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.bed_not_found

    if out == 2:
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.bed_already_used

    await log_request(request, status.HTTP_200_OK, *log_data)
    return schemas.ApiResponse(detail="Cama eliminada de la habitación")
