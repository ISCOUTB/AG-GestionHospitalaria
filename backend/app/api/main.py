from fastapi import APIRouter

from app.api.routes import beds, login, users, admins, \
doctors, patients, documents, consultations, hospitalizations

api_router = APIRouter()
api_router.include_router(beds.router, tags=["beds"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(admins.router, tags=["admins"])
api_router.include_router(doctors.router, tags=["doctors"])
api_router.include_router(patients.router, tags=["patients"])
api_router.include_router(documents.router, tags=["documents"])
api_router.include_router(consultations.router, tags=["consultations"])
api_router.include_router(hospitalizations.router, tags=["hospitalizations"])
