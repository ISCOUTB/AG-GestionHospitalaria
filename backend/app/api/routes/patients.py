from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.api.deps import (
    SessionDep,
    Patient
)

from app import models, schemas

router = APIRouter(prefix="/patient")


@router.get("/")
async def root() -> dict:
    return {"detail": "root/users/patient", "status": status.HTTP_200_OK}