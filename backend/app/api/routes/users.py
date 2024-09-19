from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.api.deps import (
    SessionDep,
    CurrentUser
)

from app import models, schemas

router = APIRouter(prefix="/users")


@router.get("/")
async def root() -> dict:
    return {"detail": "root/users", "status": status.HTTP_200_OK}


@router.get("/info")
async def get_info(current_user: CurrentUser, db:SessionDep) -> schemas.User:
    """
    Obtiene toda la información del usuario
    """
    pass


@router.put("/")
async def update_info(current_user: CurrentUser, db: SessionDep, updated_info: schemas.UserUpdate) -> schemas.models.UsersInfo:
    """
    Modifica la información no esencial de para determinado usuario
    """
    pass
