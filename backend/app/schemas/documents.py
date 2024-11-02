from pydantic import BaseModel


class Files(BaseModel):
    """
    Listado de archivos de un paciente

    Attributes:
        history (str): Nombre del archivo de la historia clínica del paciente
        orders (list[str]): Listado de nombres de los archivos de las ordenes médicas del paciente
        results (list[str]): Listado de nombres de los archivos de los resultados médicos del paciente
    """

    history: str
    orders: list[str]
    results: list[str]
