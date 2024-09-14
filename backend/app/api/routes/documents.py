from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.api.deps import (
    SessionDep,
    Admin,
    Doctor,
    Patient
)

from app import models, schemas

router = APIRouter(prefix="/documents")


@router.get("/")
async def root() -> dict:
    return {"detail": "root/documents", "status": status.HTTP_200_OK}
