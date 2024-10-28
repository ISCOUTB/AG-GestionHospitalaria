from fastapi import APIRouter

from app.api.deps import SessionDep, Admin

router = APIRouter()


@router.get("/stats", summary="Get Statistics About Hospital")
async def get_stats(current_user: Admin, db: SessionDep) -> list[float]:
    """
    Obtiene los indicadores estadísiticos del hospital.

    Los indicadores estadísitcos del hospital están listados de la siguiente manera:
        1. Porcentaje de ocupación hospitalaria.
        2. Promedios de estancia de los pacientes en el hospital.
        3. Cantidad de admisiones y altas por día.
    """
    pass
