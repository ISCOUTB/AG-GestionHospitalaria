from time import perf_counter
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import CurrentUser, SessionDep, log_request
from app.core.config import settings
from app.core.security import create_access_token

from app import schemas
from app.crud import crud_user

router = APIRouter(prefix="/login")


@router.post("/access-token")
async def login_access_token(
    request: Request,
    db: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    rol: Annotated[schemas.Roles, Body()],
) -> schemas.Token:
    """
    Obtiene el token de acceso al sistema
    """
    user_data = [form_data.username, rol]

    start_time = perf_counter()
    user_login = schemas.UserLogin(
        num_document=form_data.username, password=form_data.password, rol=rol
    )

    user = crud_user.authenticate_user(user_login, db)
    if user is None:
        process_time = perf_counter() - start_time
        log_data = [process_time, None, *user_data]
        log_request(request, status.HTTP_401_UNAUTHORIZED, *log_data)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrecto",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        number_document=user.num_document,
        rol=user.rol,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    process_time = perf_counter() - start_time

    log_data = [process_time, None, *user_data]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.get("/test-token")
async def test_token(request: Request, current_user: CurrentUser) -> schemas.models.UserRoles:
    """
    Probar el token de acceso
    """
    log_data = [0.0, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return current_user