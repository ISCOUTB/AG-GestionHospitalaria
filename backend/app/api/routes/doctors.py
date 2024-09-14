from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.api.deps import (
    SessionDep,
    Doctor
)

from app import models, schemas

router = APIRouter(prefix="/doctor")


@router.get("/")
async def root() -> dict:
    return {"detail": "root/doctor", "status": status.HTTP_200_OK}
