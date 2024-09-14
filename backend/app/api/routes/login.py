from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import CurrentUser, SessionDep
from app.core import security

from app import schemas

router = APIRouter(prefix="/login")


@router.get("/")
async def root() -> dict:
    return {"detail": "root/login", "status": status.HTTP_200_OK}


@router.post("/access-token")
async def login_access_token(db: SessionDep, 
                             form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                             rol: Annotated[schemas.Roles, Body()]) -> schemas.Token:
    """
    Obtiene el token de acceso al sistema
    """
    user_search: schemas.UserSearch = schemas.UserSearch(
        number_document=form_data.username,
        rol=rol
    )

    # Se autentica el usuario y se sigue con toda la lógica...
    pass


@router.get("/test-token")
async def test_token(current_user: CurrentUser) -> schemas.models.UserRoles:
    """
    Probar el token de acceso
    """
    return current_user
