from collections.abc import Generator
from typing import Annotated, Any
from datetime import datetime

from pymongo import MongoClient
from app.core.config import settings

import jwt
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import SessionLocal

from app import schemas
from app.api.exceptions import credentials_exception, unauthorized_exception
from app.crud import crud_user

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
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
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenPayload(
            number_document=payload.get("number_document"), rol=payload.get("rol")
        )
    except (ValidationError, InvalidTokenError):
        raise credentials_exception

    user_search = schemas.UserSearch(
        num_document=token_data.number_document, rol=token_data.rol
    )

    user = crud_user.get_user_rol(user_search, db)

    if user is None:
        raise credentials_exception

    return schemas.models.UserRoles.model_validate(user)


CurrentUser = Annotated[schemas.models.UserRoles, Depends(get_current_user)]


def get_current_admin(current_user: CurrentUser) -> schemas.models.UserRoles | None:
    if current_user.rol != "admin":
        raise unauthorized_exception

    return current_user


def get_current_doctor(current_user: CurrentUser) -> schemas.models.UserRoles | None:
    if current_user.rol != "doctor":
        raise unauthorized_exception

    return current_user


def get_current_patient(current_user: CurrentUser) -> schemas.models.UserRoles | None:
    if current_user.rol != "patient":
        raise unauthorized_exception

    return current_user


def get_current_nonpatient(
    current_user: CurrentUser,
) -> schemas.models.UserRoles | None:
    if current_user.rol == "patient":
        raise unauthorized_exception

    return current_user


Admin = Annotated[schemas.models.UserRoles, Depends(get_current_admin)]
Doctor = Annotated[schemas.models.UserRoles, Depends(get_current_doctor)]
Patient = Annotated[schemas.models.UserRoles, Depends(get_current_patient)]
NonPatient = Annotated[schemas.models.UserRoles, Depends(get_current_nonpatient)]

client = MongoClient(str(settings.MONGO_URI))
db = client[settings.MONGO_DB]
collection = db["api_logs"]

async def log_request(
        request: Request,
        response_status: int,
        process_time: float,
        body: dict[str, Any] | None,
        username: str,
        rol: schemas.Roles,
) -> None:
    log_data = {
        "username": username,
        "rol": rol,
        "timestamp": datetime.now(),
        "method": request.method,
        "url": request.url.path,
        "headers": dict(request.headers),
        "body": body,
        "process_time_ms": round(process_time * 1000, 2),
        "status_code": response_status,
    }
    collection.insert_one(log_data)
