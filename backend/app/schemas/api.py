from pydantic import BaseModel


class ApiResponse(BaseModel):
    """
    Clase para los mensajes de respuesta de la API.

    Attributes:
        detail (str): Mensaje de respuesta.
    """

    detail: str
