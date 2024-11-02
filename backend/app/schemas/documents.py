from pydantic import BaseModel
from typing import Literal


KindFiles = Literal["orders", "results"]

class AllFiles(BaseModel):
    """
    Listado de archivos de un paciente

    Attributes:
        num_document (str): Número de documento del paciente
        history (str): Nombre del archivo de la historia clínica del paciente
        orders (list[str]): Listado de nombres de los archivos de las ordenes médicas del paciente
        results (list[str]): Listado de nombres de los archivos de los resultados médicos del paciente
    """

    num_document: str
    history: str
    orders: list[str]
    results: list[str]


class Files(BaseModel):
    """
    Nombre de las ordenes medicas de un paciente

    Attributes:
        num_document (str): Número de documento del paciente
        filenames (list[str]): Listado de nombres de los archivos del paciente
        kind (Literal["orders", "results"]): Indica qué tipo de archivo se desea obtener.
    """

    num_document: str
    filenames: list[str]
    kind: KindFiles
