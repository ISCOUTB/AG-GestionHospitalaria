from typing import Any
from pydantic import BaseModel
from datetime import datetime


class ApiResponse(BaseModel):
    """
    Clase para los mensajes de respuesta de la API.

    Attributes:
        detail (str): Mensaje de respuesta.
    """

    detail: str


class ApiHistorial(BaseModel):
    """
    Clase base para obtener el historial de la API.

    Attributes:
        username (str): Nombre del usuario que realizó la operación.
        rol (str): Rol del usuario que realizó la operación.
        timestamp (datetime.datetime): Fecha y hora de la operación.
        method (str): Método de la operación.
        url (str): URL de la operación.
        headers (dict): Cabeceras de la petición de la operación.
        body (dict[str, Any] | None): Cuerpo de la petición de la operación.
        process_time_ms (float): Tiempo de procesamiento de la operación en milisegundos.
        status_code (int): Código de estado de la respuesta de la operación.
    """

    username: str
    rol: str
    timestamp: datetime
    method: str
    url: str
    headers: dict[str, Any]
    body: dict[str, Any] | None
    process_time_ms: float
    status_code: int


class Stats(BaseModel):
    """
    Clase para obtener los indicadores estadísticos del hospital.
    
    Attributes:
        percent_occupation (float): Porcentaje de ocupación hospitalaria.
        avg_stay (float): Promedio de estancia de los pacientes en el hospital.
        admissions (float): Cantidad de admisiones y altas por día en promedio.
        discharges (float): Cantidad de descargos y bajas por día en promedio.
    """

    percent_occupation: float
    avg_stay: float
    admissions: float
    discharges: float
