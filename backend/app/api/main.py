from fastapi import APIRouter

from app.api.routes import *

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(admins.router, tags=["admins"])
api_router.include_router(doctors.router, tags=["doctors"])
api_router.include_router(patients.router, tags=["patients"])
api_router.include_router(documents.router, tags=["documents"])
api_router.include_router(appointments.router, tags=["appointments"])
