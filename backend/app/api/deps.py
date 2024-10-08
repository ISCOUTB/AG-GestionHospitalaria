from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import SessionLocal

from app import schemas
from app.crud import crud_user

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V1_STR}/login/access-token'
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[Session, Depends(reusable_oauth2)]


def get_current_user(db: SessionDep, token: TokenDep) -> schemas.models.UserRoles:
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "bearer"}
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = schemas.TokenPayload(
            number_document=payload.get("number_document"),
            rol=payload.get("rol")
        )
    except (ValidationError, InvalidTokenError):
        raise credentials_exception

    user_search = schemas.UserSearch(
        num_document=token_data.number_document,
        rol=token_data.rol
    )

    user = crud_user.get_user_rol(user_search, db)
    
    if user is None:
        raise credentials_exception

    return schemas.models.UserRoles.model_validate(user)


CurrentUser = Annotated[schemas.models.UserRoles, Depends(get_current_user)]


def get_current_superuser(current_user: CurrentUser) -> schemas.models.UserRoles | None:
    if current_user.num_document == settings.FIRST_SUPERUSER:
        return current_user
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Usuario no autorizado")


def get_current_admin(current_user: CurrentUser) -> schemas.models.UserRoles | None:
    if current_user.rol != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Usuario no autorizado")
    
    return current_user


def get_current_doctor(current_user: CurrentUser) -> schemas.models.UserRoles | None:
    if current_user.rol != 'doctor':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Usuario no autorizado")
    
    return current_user


def get_current_patient(current_user: CurrentUser) -> schemas.models.UserRoles | None:
    if current_user.rol != 'patient':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Usuario no autorizado")
    
    return current_user


def get_current_nonpatient(current_user: CurrentUser) -> schemas.models.UserRoles | None:
    if current_user.rol == 'patient':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Usuario no autorizado")
    
    return current_user


Admin = Annotated[schemas.models.UserRoles, Depends(get_current_admin)]
Doctor = Annotated[schemas.models.UserRoles, Depends(get_current_doctor)]
Patient = Annotated[schemas.models.UserRoles, Depends(get_current_patient)]
SuperUser = Annotated[schemas.models.UserRoles, Depends(get_current_superuser)]  # Nada más existe un solo superuser
NonPatient = Annotated[schemas.models.UserRoles, Depends(get_current_nonpatient)]
