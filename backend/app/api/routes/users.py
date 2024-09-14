from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.api.deps import (
    SessionDep,
    Admin,
    Doctor,
    Patient,
    SuperUser
)

from app import models, schemas

router = APIRouter(prefix="/users")


@router.get("/")
async def root() -> dict:
    return {"detail": "root/users", "status": status.HTTP_200_OK}
