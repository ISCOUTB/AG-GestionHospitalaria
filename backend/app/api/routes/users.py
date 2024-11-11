from time import perf_counter

from fastapi import APIRouter, status, Request

from app.api.deps import SessionDep, CurrentUser, Admin, log_request

from app import schemas
from app.api import exceptions
from app.crud import crud_user, crud_admin, crud_document
from app.core.config import settings

router = APIRouter(prefix="/users")


@router.get("/info")
async def get_info(
    request: Request, current_user: CurrentUser, db: SessionDep
) -> schemas.UserBase:
    """
    Obtiene toda la información del usuario
    """
    start_time = perf_counter()
    info = crud_user.get_user(current_user.num_document, db)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return info


@router.get("/{num_document}")
async def get_user(
    num_document: str,
    request: Request,
    current_user: Admin,
    db: SessionDep,
    rol: bool = False,
    active: bool = True,
) -> schemas.UserBase | schemas.UserAll | None:
    """
    Obtiene la información básica de un usuario del sistema sin importar el rol
    """
    start_time = perf_counter()
    user = crud_user.get_user(num_document, db, rol, active)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    if user is None:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.user_not_found

    await log_request(request, status.HTTP_200_OK, *log_data)
    return user


@router.get("/")
async def get_users(
    request: Request,
    current_user: Admin,
    db: SessionDep,
    rol: bool = False,
    active: bool = True,
) -> list[schemas.UserBase] | list[schemas.UserAll]:
    """
    Obtiene todos los usuarios dentro del sistema.
    """
    start_time = perf_counter()
    users = crud_user.get_users(db, rol, active)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return users


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    request: Request, current_user: Admin, db: SessionDep, new_user: schemas.UserCreate
) -> schemas.ApiResponse:
    """
    Crea un nuevo usuario dentro en el sistema. No se pueden crear nuevos administradores.
    """
    body = new_user.model_dump()
    del body["password"]
    start_time = perf_counter()
    admins_bool = False
    if current_user.num_document == settings.FIRST_SUPERUSER:
        admins_bool = True

    out = crud_admin.create_user(new_user, db, admins_bool)
    if out == 1:
        process_time = perf_counter() - start_time
        log_data = [process_time, body, current_user.num_document, current_user.rol]
        await log_request(request, status.HTTP_403_FORBIDDEN, *log_data)
        raise exceptions.non_superuser

    if out == 2:
        process_time = perf_counter() - start_time
        log_data = [process_time, body, current_user.num_document, current_user.rol]
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.user_found

    if out == 3:
        process_time = perf_counter() - start_time
        log_data = [process_time, body, current_user.num_document, current_user.rol]
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.invalid_email

    if out == 4:
        process_time = perf_counter() - start_time
        log_data = [process_time, body, current_user.num_document, current_user.rol]
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.existent_phone

    if new_user.rol == "patient":
        crud_document.add_history(new_user.num_document)

    process_time = perf_counter() - start_time
    log_data = [process_time, body, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_201_CREATED, *log_data)
    return schemas.ApiResponse(detail="Usuario creado")


@router.put("/{num_document}/{rol}")
async def update_user(
    num_document: str,
    rol: schemas.Roles,
    request: Request,
    current_user: Admin,
    db: SessionDep,
    updated_info: schemas.UserUpdateAll,
) -> schemas.ApiResponse:
    """
    Actualiza la información completa de cualquier usuario dentro del sistema que no sea un administrador.
    """
    body = updated_info.model_dump()
    del body["password"]
    start_time = perf_counter()
    admins_bool = False
    if current_user.num_document == settings.FIRST_SUPERUSER:
        admins_bool = True

    user_search = schemas.UserSearch(num_document=num_document, rol=rol)
    out = crud_admin.update_user(user_search, updated_info, db, admins_bool)
    process_time = perf_counter() - start_time

    log_data = [process_time, body, current_user.num_document, current_user.rol]
    if out == 1:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.user_not_found

    if out == 2:
        await log_request(request, status.HTTP_403_FORBIDDEN, *log_data)
        raise exceptions.non_superuser

    if out == 3:
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.num_document_used

    if out == 4:
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.invalid_email

    if out == 5:
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.existent_phone

    await log_request(request, status.HTTP_200_OK, *log_data)
    return schemas.ApiResponse(detail="Información del usuario actualizada")


@router.put("/")
async def update_basic_user(
    request: Request,
    current_user: CurrentUser,
    db: SessionDep,
    updated_info: schemas.UserUpdate,
) -> schemas.ApiResponse:
    """
    Modifica la información no esencial
    """
    body = updated_info.model_dump()
    del body["password"]
    start_time = perf_counter()
    user_search: schemas.UserSearch = schemas.UserSearch(
        num_document=current_user.num_document, rol=current_user.rol
    )
    out = crud_user.update_basic_info(user_search, updated_info, db)
    process_time = perf_counter() - start_time

    log_data = [process_time, body, current_user.num_document, current_user.rol]
    if out == 1:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.user_not_found

    if out == 2:
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.invalid_email

    if out == 3:
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.existent_phone

    await log_request(request, status.HTTP_200_OK, *log_data)
    return schemas.ApiResponse(detail="Información del usuario actualizada")


@router.delete("/{num_document}/{rol}")
async def delete_user(
    num_document: str,
    rol: schemas.Roles,
    request: Request,
    current_user: Admin,
    db: SessionDep,
) -> schemas.ApiResponse:
    """
    "Elimina" a un usuario activo dentro del sistema. En realidad, lo que se hace es colocar al usuario como inactivo.
    En el caso de los pacientes que están en cama, no se pueden colocar como inactivos todavía.
    """
    start_time = perf_counter()
    admins_bool = False
    if current_user.num_document == settings.FIRST_SUPERUSER:
        admins_bool = True

    user_search: schemas.UserSearch = schemas.UserSearch(
        num_document=num_document, rol=rol
    )
    out = crud_admin.delete_user(user_search, db, admins_bool)
    process_time = perf_counter() - start_time

    log_data = [process_time, None, current_user.num_document, current_user.rol]
    if out == 1:
        await log_request(request, status.HTTP_404_NOT_FOUND, *log_data)
        raise exceptions.user_not_found

    if out == 2:
        await log_request(request, status.HTTP_403_FORBIDDEN, *log_data)
        raise exceptions.non_superuser

    if out == 3:
        await log_request(request, status.HTTP_409_CONFLICT, *log_data)
        raise exceptions.patient_in_bed

    await log_request(request, status.HTTP_200_OK, *log_data)
    return schemas.ApiResponse(detail="Usuario eliminado")
