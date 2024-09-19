from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f'{route.tags[0]}-{route.name}'


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
    generate_unique_id_function=custom_generate_unique_id,
    openapi_tags=[
        {
            "name": "login",
            "description": "Acceso al sistema"
        },
        {
            "name": "users",
            "description": "Acciones de todos los usuarios"
        },
        {
            "name": "admins",
            "description": "Acciones solo para administradores"
        },
        {
            "name": "doctors",
            "description": "Acciones solo para doctores"
        },
        {
            "name": "patients",
            "description": "Acciones solo para pacientes"
        },
        {
            "name": "documents",
            "description": "Acciones para los documentos médicos de los pacientes"
        },
        {
            "name": "appointments",
            "description": "Acciones sobre las citas médicas de los pacientes en el hospital. Incluye consultas normales y urgencias"
        }
    ]
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
