from datetime import date, datetime
from time import perf_counter

from fastapi import APIRouter, Request, status

from app.api.deps import SessionDep, Admin, collection, log_request

from app import schemas

router = APIRouter()


@router.get("/stats", summary="Get Statistics About Hospital")
async def get_stats(current_user: Admin, db: SessionDep) -> schemas.Stats:
    """
    Obtiene los indicadores estadísiticos del hospital.

    Los indicadores estadísitcos del hospital están listados de la siguiente manera:
        1. Porcentaje de ocupación hospitalaria.
        2. Promedios de estancia de los pacientes en el hospital.
        3. Cantidad de admisiones y altas por día.
    """
    pass


@router.get("/api-historial")
async def get_api_historial(
    request: Request,
    current_user: Admin,
    limit: int = -1,
    start_date: date | None = None,
    end_date: date | None = None,
    method: str | None = None,
    url: str | None = None,
) -> list[schemas.ApiHistorial]:
    """
    Obtiene el historial de la API guardadas en la base de datos en mongodb. 
    """
    start_time = perf_counter()

    if limit <= 0:
        limit = collection.count_documents({})

    date_filter = {}

    if start_date is not None:
        date_filter["$gte"] = datetime.combine(start_date, datetime.min.time())
    if end_date is not None:
        date_filter["$lte"] = datetime.combine(end_date, datetime.max.time())

    query = {"timestamp": date_filter} if date_filter else {}    

    if method is not None:
        query["method"] = method.upper()
    if url is not None:
        query["url"] = url

    documents = collection.find(query).limit(limit)

    result: list[schemas.ApiHistorial] = []
    for document in documents:
        result.append(
            schemas.ApiHistorial(
                username=document["username"],
                rol=document["rol"],
                timestamp=document["timestamp"],
                method=document["method"],
                url=document["url"],
                headers=document["headers"],
                body=document["body"],
                process_time_ms=document["process_time_ms"],
                status_code=document["status_code"],
            )
        )

    process_time = perf_counter() - start_time
    log_data = [process_time, None, current_user.num_document, current_user.rol]
    await log_request(request, status.HTTP_200_OK, *log_data)
    return result
